# Sentinel-OOB Agent Failure Semantics (v0.1)

## Agent Role
The agent is a liveness signal, not a security decision-maker.

## Failure Interpretation
- Agent termination is treated as suspicious
- Agent silence is treated as potential compromise
- Agent does not attempt self-recovery or retries

## Design Rules
- Agent must be simple and noisy
- Agent must not suppress or delay heartbeats
- Agent must not store state locally
- Agent failure must surface externally via silence

## Non-Goals
- Agent self-protection against admin attackers
- Agent stealth or persistence
- Agent recovery after compromise

## Security Principle
If the agent stops speaking, the system assumes risk.
