# Makefile for Sentinel-OOB

.PHONY: all build test clean server agent

# Default target
all: build

# Build both components
build: agent server

# Build Go agent
agent:
	cd agent && go build -o ../bin/sentinel-agent main.go

# Install Python dependencies and check server
server:
	cd server && pip install -r requirements.txt

# Run tests (placeholder)
test:
	@echo "Run adversarial tests manually: see docs/tests/"

# Clean build artifacts
clean:
	rm -rf bin/
	cd agent && go clean
	cd server && rm -rf __pycache__

# Run server
run-server:
	cd server && python main.py

# Run agent (debug mode)
run-agent:
	cd agent && go run main.go