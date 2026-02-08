package main

import (
	"bytes"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"syscall"
	"time"
	"unsafe"

	"github.com/google/uuid"
	"golang.org/x/sys/windows/svc"
	"golang.org/x/sys/windows/svc/debug"
)

/* =========================
   CONFIG
   ========================= */

const (
	serverURL    = "http://localhost:8000/heartbeat"
	agentVersion = "0.2"
	interval     = 10 * time.Second
)

var hmacSecret string

/* =========================
   WINDOWS STRUCT
   ========================= */

type LASTINPUTINFO struct {
	CbSize uint32
	DwTime uint32
}

/* =========================
   HEARTBEAT
   ========================= */

type Heartbeat struct {
	HostID          string  `json:"host_id"`
	Timestamp       float64 `json:"timestamp"`
	Locked          bool    `json:"locked"`
	InactiveSeconds int     `json:"inactive_seconds"`
	Network         string  `json:"network"`
	AgentVersion    string  `json:"agent_version"`
	Signature       string  `json:"signature"`
}

/* =========================
   SERVICE
   ========================= */

type sentinelService struct {
	hostID string
	stopCh chan struct{}
}

func (s *sentinelService) Execute(args []string, r <-chan svc.ChangeRequest, status chan<- svc.Status) (bool, uint32) {
	status <- svc.Status{State: svc.StartPending}
	status <- svc.Status{State: svc.Running, Accepts: svc.AcceptStop | svc.AcceptShutdown}

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			sendHeartbeat(s.hostID)
		case c := <-r:
			if c.Cmd == svc.Stop || c.Cmd == svc.Shutdown {
				close(s.stopCh)
				status <- svc.Status{State: svc.StopPending}
				return false, 0
			}
		}
	}
}

/* =========================
   HOST ID
   ========================= */

func getHostID() (string, error) {
	dir, err := os.UserConfigDir()
	if err != nil {
		return "", err
	}

	path := filepath.Join(dir, "sentinel-oob-host-id")

	if data, err := os.ReadFile(path); err == nil {
		return string(data), nil
	}

	id := uuid.New().String()
	if err := os.WriteFile(path, []byte(id), 0600); err != nil {
		return "", err
	}

	return id, nil
}

/* =========================
   STATE COLLECTION
   ========================= */

func isSessionLocked() bool {
	user32 := syscall.NewLazyDLL("user32.dll")
	proc := user32.NewProc("GetForegroundWindow")
	hwnd, _, _ := proc.Call()
	return hwnd == 0
}

func getInactiveSeconds() int {
	user32 := syscall.NewLazyDLL("user32.dll")
	proc := user32.NewProc("GetLastInputInfo")

	var info LASTINPUTINFO
	info.CbSize = uint32(unsafe.Sizeof(info))

	ret, _, _ := proc.Call(uintptr(unsafe.Pointer(&info)))
	if ret == 0 {
		return -1
	}

	kernel32 := syscall.NewLazyDLL("kernel32.dll")
	getTick := kernel32.NewProc("GetTickCount64")
	nowTicks, _, _ := getTick.Call()

	return int((uint64(nowTicks) - uint64(info.DwTime)) / 1000)
}

func getNetworkContext() string {
	cmd := exec.Command("powershell", "-Command", "(Get-WmiObject Win32_ComputerSystem).PartOfDomain")
	out, err := cmd.Output()
	if err != nil {
		return "UNTRUSTED"
	}
	if strings.Contains(string(out), "True") {
		return "TRUSTED"
	}
	return "UNTRUSTED"
}

/* =========================
   CANONICAL STRING (MUST MATCH SERVER)
   ========================= */

func canonicalString(hb Heartbeat) string {
	lockedStr := "False"
	if hb.Locked {
		lockedStr = "True"
	}
	return fmt.Sprintf(
		"%s|%d|%s|%d|%s|%s",
		hb.HostID,
		int64(hb.Timestamp),
		lockedStr,
		hb.InactiveSeconds,
		hb.Network,
		hb.AgentVersion,
	)
}

/* =========================
   SIGNING
   ========================= */

func signHeartbeat(hb Heartbeat) (string, error) {
	secret := os.Getenv("SENTINEL_HMAC_SECRET")
	if secret == "" {
		return "", fmt.Errorf("SENTINEL_HMAC_SECRET not set")
	}

	data := canonicalString(hb)

	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(data))

	return hex.EncodeToString(mac.Sum(nil)), nil
}

/* =========================
   SEND
   ========================= */

func sendHeartbeat(hostID string) {
	hb := Heartbeat{
		HostID:          hostID,
		Timestamp:       float64(time.Now().Unix()),
		Locked:          isSessionLocked(),
		InactiveSeconds: getInactiveSeconds(),
		Network:         getNetworkContext(),
		AgentVersion:    agentVersion,
	}

	signature, err := signHeartbeat(hb)
	if err != nil {
		return
	}
	hb.Signature = signature

	data, _ := json.Marshal(hb)
	resp, err := http.Post(serverURL, "application/json", bytes.NewBuffer(data))
	if err != nil {
		fmt.Printf("Error sending heartbeat: %v\n", err)
		return
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		fmt.Printf("Heartbeat failed: %d %s\n", resp.StatusCode, resp.Status)
	} else {
		fmt.Println("Heartbeat sent successfully")
	}
}

/* =========================
   MAIN
   ========================= */

func main() {
	// 🔒 Fail hard if secret missing
	hmacSecret = os.Getenv("SENTINEL_HMAC_SECRET")
	if hmacSecret == "" {
		panic("SENTINEL_HMAC_SECRET not set")
	}

	hostID, err := getHostID()
	if err != nil {
		panic(err)
	}

	service := &sentinelService{
		hostID: hostID,
		stopCh: make(chan struct{}),
	}

	// ✅ FIX: capture both return values
	isService, err := svc.IsWindowsService()
	if err != nil {
		panic(err)
	}

	if isService {
		err = svc.Run("SentinelOOB", service)
		if err != nil {
			panic(err)
		}
	} else {
		err = debug.Run("SentinelOOB", service)
		if err != nil {
			panic(err)
		}
	}
}
