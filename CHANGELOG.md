# Changelog

All notable changes to Sentinel-OOB will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Adversarial test plan and results in `docs/tests/`
- Normalized documentation structure

### Changed
- Moved docs to subfolders: `specs/`, `tests/`, `releases/`

## [0.4.0] - 2026-01-31

### Added
- Adversarial validation phase
- Multi-channel alert delivery (webhook, Telegram, email)
- HMAC signature verification for telemetry integrity
- Silence detection with presence context

### Changed
- Canonical string format for boolean fields (True/False)
- Agent heartbeat includes network trust context

### Fixed
- Compilation errors in Go agent
- Import conflicts in Python server

## [0.3.0] - 2025-XX-XX

### Added
- Email alert channel
- Audit logging

## [0.2.0] - 2025-XX-XX

### Added
- Webhook alert delivery
- Telegram integration

## [0.1.0] - 2025-XX-XX

### Added
- Basic heartbeat and silence detection
- Initial agent and server implementation