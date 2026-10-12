# Ingress original-media custody and restore plan — 2026-10-12

Status: inventory complete within the two user-content roots; original-media content hashing, custody transfer and restore are planned, not executed. Keep all originals and prior custody copies. PRs #2 and #3 remain open for review.

## Inventory evidence

The [aggregate inventory](../../docs/evidence/ingress-original-media-inventory-2026-10-12.json) records 347 regular files, 281,534,336,361 logical bytes, 12 directories, no symlinks or special files, zero enumeration errors and zero file changes on a second stat pass.
- time-moment-brief: 253 files / 181,588,707,123 bytes.
- backwards-up-hill: 94 files / 99,945,629,238 bytes.

The exact original-path ledger is private:
 /Users/4jp/Workspace/limen/.limen-private/custody-staging/ingress-inventory-20261012-56876a482ab8/inventory.json
SHA-256: 9cb729dcf38be13c7faff5e891cbfc9c1e126b833591ef026e773be6010fefe6.

All entries inside both roots are included, including MP4, 360, WAV, JPG, LRV, LRF, THM and extensionless files. Volume service metadata (.Spotlight-V100, .Trashes, .fseventsd and root .DS_Store) is excluded. File extensions do not establish original-versus-derivative provenance: preserve everything in scope. This is a metadata inventory, not camera-card completeness, content validation or a point-in-time filesystem snapshot.

## Capacity and physical independence

Ingress UUID 8E4C5386-7281-4E65-BC65-363C08FAAE50 and Archive4T UUID 45C8AA30-307B-41E2-908D-5112E93B4AF5 both reside on physical disk7. T7Recovery UUID 0287E02B-989A-419B-A7CA-B4BCE4ECA1FF resides on disk9. Re-resolve physical identifiers by UUID before each operation; disk numbers can change.

At inventory time T7Recovery had 315,296,735,232 bytes free, leaving 33,762,398,871 bytes after logical payload, or 12,287,562,391 bytes beyond the proposed 20 GiB reserve. Metadata, extended attributes and concurrent writers can consume this margin; admission uses fresh free space and measured overhead, not this snapshot alone.

Local staging had only 28,596,731,904 bytes free. Do not attempt a complete local restore. Archive4T had 1,442,331,160,576 bytes free and can host the complete restore in a new private directory. This establishes restore from disk9 onto disk7, not a third independent backup device.

## Serialized execution

1. Reconfirm mounts by UUID, physical separation, free space, no active writer within the two source roots, and the full inventory path/size/mtime/inode/device tuple. Re-enumerate for additions and removals too. If the source changes, retain this inventory and issue a new version; do not silently reuse it.
2. Create unique mode-0700 roots under T7Recovery/limen-custody and Archive4T/limen-custody, plus a fresh private local receipt directory outside vendor runtime state. Never reuse the six-file derivative custody directory or overwrite any destination. Preserve exact root-relative names and empty directories. Check path collisions, ACLs, flags, extended attributes and resource forks before selecting the metadata-preserving copy method; include their verification in receipts.
3. Hash each source file with streaming SHA-256 and stat before/after reading. Record the digest and metadata in the private manifest. Do not deduplicate away distinct original paths. Refuse source drift and retain failed-attempt evidence.
4. Copy serially into exclusively created destination files on T7Recovery; use per-file temporary names in the new custody tree and promote only after completed readback. Never use delete, mirror, prune or overwrite modes. Verify every destination data-fork hash by reopening it from the device, and verify metadata/resource forks separately. Recheck free-space reserve throughout.
5. Restore every verified original-path entry FROM T7Recovery into the fresh Archive4T restore tree. Reopen and hash every restored file independently against the frozen source manifest; verify names, directory inventory and metadata/resource forks. No restore operation targets Ingress or an existing source tree.
6. Independently enumerate both destinations and require exact manifest membership, byte totals, all file digests, metadata checks, no unaccounted partials and no missing paths. Re-enumerate source and compare it with the frozen inventory and hash-pass metadata. Retain private full receipts on both devices and local staging; publish only sanitized aggregate evidence and receipt hashes.
7. Report custody verified only when all 347 original paths (or a newly versioned inventory) pass both device readback and full restore. Preserve source originals regardless of success. Keep PRs open; no media publication, retirement, cleanup or merge is authorized by this plan.

## Bounded attempts and interrupted work

Use one recovery writer and one I/O workload. Before bulk hashing or copying, use the existing Limen recovery/admission rail and current ownership evidence; an unchanged admission denial is a stop, not a retry loop. Each attempt has a 30-minute wall bound, with at most 10 minutes verification and 120 cumulative agent-minutes per approved outcome including restarts. Record a hard process deadline, low-priority execution, exact completed-file ledger and checkout retention. A single file operation also needs a deadline and free-space guard; interrupted partials are retained and not counted as verified.

Measure throughput on a bounded representative tranche without deleting its verified copy. Compute remaining source-hash, transfer, readback and restore time from observed rates before admitting further work. A full cycle reads roughly six payload lengths across hash/copy/readback/restore/final-source verification, so it may exceed one attempt or the cumulative allowance. At exhaustion, retain all evidence and stop; checkpointing is not completed custody. Resume only under the applicable renewed budget/ownership, checking every existing completed entry before reuse.

## Acceptance exclusions

Full decoding/playback, camera-card/source completeness, headset/XR acceptance, and authenticity of camera/date labels remain separate. Archive4T being on the same disk as Ingress must remain visible in every final receipt. The six-file derivative recovery remains valid only for its previously recorded bounded set.
