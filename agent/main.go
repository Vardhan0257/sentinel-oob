package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"os"
	"fmt"
	"path/filepath"
	"syscall"
	"time"
	"unsafe"
	"github.com/google/uuid"
	"golang.org/x/sys/windows/svc"
	"golang.org/x/sys/windows/svc/debug"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
)

const (
	serverURL    = "http://localhost:8000/heartbeat"
	agentVersion = "0.2"
	interval     = 10 * time.Second
)

type LASTINPUTINFO struct {
	CbSize uint32
	DwTime uint32
}

type Heartbeat struct {
	HostID           string  `json:"host_id"`
	Timestamp        float64 `json:"timestamp"`
	Locked           bool    `json:"locked"`
	InactiveSeconds  int     `json:"inactive_seconds"`
	AgentVersion     string  `json:"agent_version"`
	Signature string `json:"signature"`
}


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

		case <-s.stopCh:
			status <- svc.Status{State: svc.StopPending}
			return false, 0
		}
	}
}

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

func isSessionLocked() (bool, error) {
	user32 := syscall.NewLazyDLL("user32.dll")
	proc := user32.NewProc("GetForegroundWindow")

	hwnd, _, err := proc.Call()
	if hwnd == 0 {
		return true, nil
	}
	if err != syscall.Errno(0) {
		return false, err
	}
	return false, nil
}

func getNetworkContext() string {
	// v0.2 heuristic: Wi-Fi treated as untrusted
	// Refined later
	return "UNTRUSTED"
}

func signHeartbeat(payload []byte) (string, error) {
	secret := os.Getenv("SENTINEL_SHARED_SECRET")
	if secret == "" {
		return "", fmt.Errorf("SENTINEL_SHARED_SECRET not set")
	}

	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write(payload)
	return hex.EncodeToString(mac.Sum(nil)), nil
}


func sendHeartbeat(hostID string) {
	locked, err := isSessionLocked()
	if err != nil {
		locked = true // fail-safe: assume absent
	}
	inactive, err := getInactiveSeconds()
	if err != nil {
		inactive = -1 // fail-safe marker
	}
	println("inactive_seconds =", inactive)

	hb := Heartbeat{
	HostID:          hostID,
	Timestamp:       float64(time.Now().Unix()),
	Locked:          locked,
	InactiveSeconds: inactive,
	AgentVersion:    agentVersion,
	}

	// Marshal unsigned payload
	unsigned, err := json.Marshal(hb)
	if err != nil {
		return
	}

	// Sign
	sig, err := signHeartbeat(unsigned)
	if err != nil {
		return
	}

	hb.Signature = sig

	// Marshal signed payload
	data, err := json.Marshal(hb)
	if err != nil {
		return
	}

	http.Post(serverURL, "application/json", bytes.NewBuffer(data))
}

func main() {
	hostID, err := getHostID()
	if err != nil {
		panic(err)
	}

	service := &sentinelService{
		hostID: hostID,
		stopCh: make(chan struct{}),
	}

	isService, err := svc.IsWindowsService()
	if err != nil {
		panic(err)
	}

	if isService {
		svc.Run("SentinelOOB", service)
	} else {
		debug.Run("SentinelOOB", service)
	}
}

func getInactiveSeconds() (int, error) {
	user32 := syscall.NewLazyDLL("user32.dll")
	proc := user32.NewProc("GetLastInputInfo")

	var info LASTINPUTINFO
	info.CbSize = uint32(unsafe.Sizeof(info))

	ret, _, err := proc.Call(uintptr(unsafe.Pointer(&info)))
	if ret == 0 {
		return 0, err
	}

	// GetTickCount64 gives ms since boot (same reference as DwTime)
	kernel32 := syscall.NewLazyDLL("kernel32.dll")
	getTick := kernel32.NewProc("GetTickCount64")

	nowTicks, _, _ := getTick.Call()
	now := uint64(nowTicks)


	lastInput := uint64(info.DwTime)

	return int((now - lastInput) / 1000), nil
}

