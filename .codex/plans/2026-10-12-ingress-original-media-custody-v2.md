# External original-media custody attempt — 2026-10-12

The human authorized running custody outside Codex and gracefully closing it to clear admission. This is one bounded attempt; it does not renew the cumulative allowance or authorize recurring work.

The private supervisor is at locator external-custody-20261012-s2phtu6a under the existing private custody-staging root. It holds a SHA-256-pinned runner snapshot, closes Codex by AppleEvent, confirms normal app exit, allows 30 seconds for pressure to settle, then invokes the persistent runner once. The runner acquires a real heavy lease after fresh metadata, open-handle, UUID and capacity checks. Denied admission stops the attempt. The supervisor reopens Codex after completion, failure or timeout.

Budget: charge a conservative 2,700 prior agent-seconds to this outcome; allow 1,200 runner seconds and 540 verification seconds, reserving the remaining portion of the 30-minute attempt for preparation, cleanup and reporting. No automatic next tranche. A hard supervisor timeout bounds its own runner process group only; it does not signal other work.

Each file advances through source SHA-256, exclusive T7Recovery copy, independent device readback with metadata verification, Archive4T restore and independent restore verification. Completed entries bind destination size, mtime, inode, device and metadata. A later explicitly continued attempt can reuse matching receipts with cumulative accounting; changed entries fail closed. Partial files and immutable per-attempt receipts remain retained.

The supervisor's private supervisor-receipt.json and runner-output.jsonl identify the complete private custody receipt. A single scheduled readback will inspect those files, publish a sanitized result to PR #3 and pause the existing heartbeat. It must not start a second custody attempt. Full success means all 347 original paths pass every stage; a bounded partial result must remain labeled incomplete. Preserve originals and keep PRs #2 and #3 open.
