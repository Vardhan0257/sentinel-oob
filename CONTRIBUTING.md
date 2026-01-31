# Contributing to Sentinel-OOB

Thank you for your interest in contributing to Sentinel-OOB! This document outlines the process for contributing.

## Code of Conduct

This project follows a simple code of conduct: be respectful, constructive, and focused on security and reliability.

## How to Contribute

### Reporting Issues
- Use GitHub Issues for bugs, security concerns, or feature requests.
- Provide detailed steps to reproduce.
- For security issues, see `SECURITY.md`.

### Development Setup

1. Clone the repository.
2. For agent: `cd agent; go mod tidy; go build`
3. For server: `cd server; pip install -r requirements.txt; python main.py`
4. Set environment variables as per `server/config.example.env`.

### Submitting Changes

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes, ensuring tests pass.
4. Update documentation if needed.
5. Commit with clear messages.
6. Push and create a Pull Request.

### Guidelines

- Follow existing code style (Go: standard, Python: PEP 8).
- Add tests for new features.
- Update `CHANGELOG.md` for changes.
- Ensure adversarial tests still pass.

## Architecture Decisions

- Agent: Minimal, untrusted, sends signed heartbeats.
- Server: Stateless, verifies signatures, detects silence.
- Alerts: Out-of-band, multi-channel.

See `docs/specs/architecture.md` for details.