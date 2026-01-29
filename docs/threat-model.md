# Sentinel-OOB Threat Model (v0.1)

## Assets Protected
- Integrity of endpoint security visibility
- Reliability of alert delivery
- User awareness during unattended periods

## Adversary Capabilities
- Physical or local access to an unlocked or unattended system
- Ability to dismiss local security prompts
- Ability to terminate user-level processes
- Ability to establish persistence after delay

## Adversary Limitations
- Cannot instantly suppress all security telemetry
- Cannot immediately disable off-host monitoring
- Cannot retroactively delete out-of-band alerts

## In-Scope Attacks
- Evil-maid attacks on unattended devices
- Local attacker dismissing security warnings
- Silent compromise during lock or idle periods

## Out-of-Scope Attacks
- Kernel-level rootkits
- Firmware compromise
- Air-gapped network isolation
- Nation-state persistent attackers

## Assumptions
- Endpoint can emit at least one heartbeat before compromise
- Silence is more indicative of compromise than benign failure
- User receives and reviews out-of-band alerts

## Security Posture
Sentinel-OOB assumes compromise on silence.
