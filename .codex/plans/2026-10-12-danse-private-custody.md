# Danse private custody attempt

Authorized scope: preserve the current Danse checkout, local-only refs, stash and
ignored material; verify two independent copies and a clean restore; publish only
redacted evidence; retain originals and both open PRs.

1. Retain the source Git store intact, including refs, stash reflogs and objects.
   Copy the complete standalone checkout rather than a HEAD-only bundle. Never
   edit source remotes, refs, files or native archival names.
2. Inventory all nodes without following links. Keep literal paths, refs and
   filenames in private mode-0700 staging outside vendor runtime directories.
   Preserve literal symlinks; refuse special nodes and external Git dependencies.
3. Prove T7Recovery and Archive4T resolve to independent physical disks using
   Danse's native medium verifier. Check capacity with a 20 GiB reserve.
4. Acquire a fresh heavy lease in the runner process. Bound the attempt to
   1,200 seconds and hash/copy verification to 600 seconds; refresh/release the
   lease, retain all partials and refuse existing destination names.
5. Verify byte hashes, membership, mode, timestamps, ownership, flags, ACLs and
   extended attributes. Restore from the second copy into a new private root;
   compare all refs, both stash reflog entries, HEAD, branch, remotes and tracked
   status, then run Git fsck. Reject source drift before/during copying.
6. Commit and push only runner, fixture checks, plan and redacted receipts to
   PR #3. Retain PR #2 and PR #3 for review; no merge or reclamation.

## Checkpoint

The fresh acquire was denied (`swap-fraction`, `disk-throughput`, `vitals-shed`).
No source payload was hashed or copied. Two preliminary metadata attempts and
their private receipts are retained. Fixture checks are local test evidence,
not Danse custody. See docs/danse-private-custody.md for exact bounds and retry
predicate. Stop this attempt; do not retry unchanged pressure or override policy.
