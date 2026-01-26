# Threat Model — Sentinel-OOB

## Goal
Detect silent endpoint compromise by treating agent silence as a security signal.

## In Scope
- Local interaction attacks
- Physical access during unattended windows
- Alert dismissal or suppression
- Agent termination or network isolation

## Out of Scope
- Kernel-level rootkits
- Firmware or bootkits
- Persistent admin-level attackers
- Malware detection or prevention

## Core Assumption
If an unattended endpoint stops sending heartbeats, compromise is assumed.
