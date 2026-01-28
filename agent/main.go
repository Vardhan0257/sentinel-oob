package main

import (
	"fmt"
	"os"
	"path/filepath"
	"syscall"
	"github.com/google/uuid"
)

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

// Windows lock state detection
func isSessionLocked() (bool, error) {
	user32 := syscall.NewLazyDLL("user32.dll")
	proc := user32.NewProc("GetForegroundWindow")

	hwnd, _, err := proc.Call()
	if hwnd == 0 {
		// No foreground window usually means locked session
		return true, nil
	}
	if err != syscall.Errno(0) {
		return false, err
	}
	return false, nil
}

func main() {
	hostID, err := getHostID()
	if err != nil {
		panic(err)
	}

	locked, err := isSessionLocked()
	if err != nil {
		panic(err)
	}

	fmt.Println("Sentinel-OOB agent")
	fmt.Println("host_id:", hostID)
	fmt.Println("locked:", locked)
}
