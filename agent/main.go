package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"path/filepath"
	"syscall"
	"time"

	"github.com/google/uuid"
)

const (
	serverURL    = "http://localhost:8000/heartbeat"
	agentVersion = "0.1"
	interval     = 10 * time.Second
)

type Heartbeat struct {
	HostID       string  `json:"host_id"`
	Timestamp    float64 `json:"timestamp"`
	Locked       bool    `json:"locked"`
	AgentVersion string  `json:"agent_version"`
}

/*
Stable host_id persisted locally.
One-time generation, reused forever.
*/
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

/*
Very simple presence heuristic:
- No foreground window → assume locked / unattended
*/
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

func sendHeartbeat(hostID string) error {
	locked, err := isSessionLocked()
	if err != nil {
		return err
	}

	hb := Heartbeat{
		HostID:       hostID,
		Timestamp:    float64(time.Now().Unix()),
		Locked:       locked,
		AgentVersion: agentVersion,
	}

	data, err := json.Marshal(hb)
	if err != nil {
		return err
	}

	resp, err := http.Post(serverURL, "application/json", bytes.NewBuffer(data))
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return fmt.Errorf("unexpected status: %s", resp.Status)
	}

	return nil
}

func main() {
	hostID, err := getHostID()
	if err != nil {
		panic(err)
	}

	fmt.Println("Sentinel-OOB agent started:", hostID)

	// Blocking heartbeat loop — service compatible
	for {
		if err := sendHeartbeat(hostID); err != nil {
			panic(err)
		}
		time.Sleep(interval)
	}
}
