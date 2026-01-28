package main

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/google/uuid"
)

func getHostID() (string, error) {
	dir, err := os.UserConfigDir()
	if err != nil {
		return "", err
	}

	path := filepath.Join(dir, "sentinel-oob-host-id")

	// If host_id already exists, reuse it
	if data, err := os.ReadFile(path); err == nil {
		return string(data), nil
	}

	// Otherwise generate and persist
	id := uuid.New().String()
	if err := os.WriteFile(path, []byte(id), 0600); err != nil {
		return "", err
	}

	return id, nil
}

func main() {
	hostID, err := getHostID()
	if err != nil {
		panic(err)
	}

	fmt.Println("Sentinel-OOB agent host_id:", hostID)
}
