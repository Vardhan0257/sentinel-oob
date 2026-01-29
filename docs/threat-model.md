# Sentinel-OOB Threat Model

## Assets
- Integrity of alert delivery
- Timely user awareness
- Off-host audit visibility

## Attacker Capabilities
- Local interactive access
- Ability to terminate user-space processes
- Ability to dismiss UI alerts
- Ability to unplug network temporarily

## Attacker Limitations
- No guaranteed kernel persistence
- No control over external alert channels
- No retroactive deletion of off-host alerts

## In-Scope Attacks
- Evil-maid attacks
- Unattended endpoint compromise
- Silent dismissal of security prompts
- Process termination of agents

## Out-of-Scope Attacks
- Kernel rootkits
- Firmware compromise
- Nation-state persistence
- Air-gapped isolation

## Design Assumption

Once kernel-level persistence is achieved,
Sentinel-OOB provides **no guarantees**.

Silence during high-risk windows is treated as compromise.
