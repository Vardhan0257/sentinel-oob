# Heartbeat Signing Specification

## Algorithm
HMAC using SHA-256.

## Shared Secret
Provided via environment variable:
- Agent: SENTINEL_SHARED_SECRET
- Server: SENTINEL_SHARED_SECRET

## Signed Data
The canonical JSON serialization of the heartbeat payload,
excluding the `signature` field.

## Signature Field
A hex-encoded HMAC-SHA256 digest.

## Verification Rule
If signature verification fails:
- Heartbeat is discarded
- No state is updated
- Silence detection proceeds normally

## Rationale
HMAC provides integrity and authenticity with minimal complexity
and no asymmetric key management.
