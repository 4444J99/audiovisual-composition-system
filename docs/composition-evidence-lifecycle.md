# Composition evidence lifecycle

Review correction on 2026-10-12. This changes acceptance record handling, not
source admission, playback, rendering, panning or existing measurement tolerances.

Every completed new attempt is written exclusively to its UUID path with no write
permission bits. A passed canonical receipt is an exclusive independent copy,
also read-only. Existing canonical receipts cannot be overwritten by publication.
Changing one pathname's bytes cannot change the other's historical record through
a shared inode. Existing passed historical receipts are retained unchanged.

Verification has a 60-second asynchronous deadline. Expiry aborts the operation
and enters cleanup instead of terminating inside the timer. Browser and HTTP
server shutdown run together, with a five-second cleanup bound; HTTP connections
are closed. Late browser launch observes cancellation and closes its browser.
Failures, including cleanup failure or cleanup timeout, retain a failed attempt
and never publish a passed canonical receipt. The CLI exits 124 for verification
deadline expiry, or 1 for another failure, only after cleanup and persistence have
settled. This is a 65-second asynchronous lifecycle bound; synchronous filesystem
operations remain ordinary blocking Node operations.

Twelve Node tests pass: the original six admission/measurement guards plus six
lifecycle cases covering independent read-only publication, no-clobber behavior,
deadline cleanup of an actual loopback server, cleanup rejection, hung cleanup and
ordinary verification failure. These tests use temporary synthetic records and
no private media. They establish lifecycle behavior, not a fresh browser-media run.

The October 10 v3 receipt names verifier SHA-256
`a1771e11a43f4c824661f06685bf30c5ad31dd3fff3ee50326a3a18d9c656d30`.
That exact verifier is recoverable from ancestor `c8e2fb9` (also `773f042`). The
later admission-path relocation and this lifecycle correction have distinct
verifier hashes. Historical acceptance remains bound to its historical program;
new runs record their own current verifier hash. No receipt has been rewritten to
claim acceptance of changed executable bytes.

The remaining source, device, custody and artist gates retain their existing
owners in the [composition report](tmb-spatial-integration-report.md) and
[workstream continuation](workstream-continuation.md).
