## Contributing to Sentinel-OOB

Thanks for your interest in contributing — we appreciate improvements of all kinds.

### Getting started
- Fork the repo and create a branch named `feature/xxx` or `fix/yyy`.
- Run the server and agent locally where applicable. See `README.md` for quick start steps.

### Code style
- Python: follow PEP8; use `black` for formatting and `flake8` for linting.
- Go: follow `gofmt` / `go vet`.

### Tests
- Add unit tests for any new behavior. For server Python code, use `pytest`.
- Ensure tests pass locally before opening a PR.

### Commits
- Write clear commit messages. Use an imperative verb: `Add`, `Fix`, `Improve`.
- Squash or rebase when appropriate; keep PR history readable.

### Pull requests
- Open a PR against `main` with a descriptive title and summary.
- Include: what changed, why, and how to test.
- Add issue references if the PR resolves an existing issue (e.g. `Fixes #123`).

### Review process
- Expect at least one maintainer review. Address comments with follow-up commits.
- Small, focused PRs merge faster.

### Issues
- Open issues for bugs, feature requests, or docs improvements. Provide reproduction steps and logs.

### Security disclosures
- For security issues, contact the maintainers privately as described in `SECURITY.md`.

### Local development tips
- Use virtual environments for Python: `python -m venv .venv` and `pip install -r server/requirements.txt`.
- For Go, ensure `go` toolchain is in PATH and run `go test ./...` in `agent/`.

### CI and quality
- We welcome adding CI (GitHub Actions) workflows for tests and linting. Please add a workflow under `.github/workflows/`.

### Want to help but not sure where?
- Browse open issues labeled `good first issue` or `help wanted`.
- Small documentation fixes and tests are great first contributions.

Thank you for contributing — every improvement helps!
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