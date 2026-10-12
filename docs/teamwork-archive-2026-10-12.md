# Stale teamwork archive — 2026-10-12

Archived only `.agents/teamwork/`: 588 files, 124 directories and 2,755,048 file bytes. No open handles or process path references were found before archiving or immediately before moving the folder. Source inventories remained stable during backup and restoration verification. Historical instruction files were treated as records.

The original tree was moved intact to `/Users/4jp/Workspace/limen/.limen-private/custody-staging/ace-teamwork-archive-20261012-org3p0jo/original-tree/.agents/teamwork`. Nothing was deleted. Other agent state and source checkouts were untouched; this same-volume move does not free disk space.

An encrypted snapshot is on the independent T7Recovery device at `/Volumes/T7Recovery/limen-custody/ace-teamwork-archive-20261012-org3p0jo/snapshot.tar.age`. It uses the existing independently escrowed recovery key. The external copy was read back, decrypted and extracted into a separate private directory. Every path, file digest and recorded metadata field matched, including extended attributes (zero differences). Encrypted manifest, original extended-attribute sidecar and receipt accompany it.

Recovery instructions are in `/Users/4jp/Workspace/limen/.limen-private/custody-staging/ace-teamwork-archive-20261012-org3p0jo/RESTORE.md`. Retrieve the existing key from the 1Password Personal document identified in [the escrow receipt](evidence/unversioned-key-escrow-2026-10-12.json). Restore into a separate private directory for inspection before placing historical agent instructions into any active workspace.

See [the sanitized verification receipt](evidence/teamwork-archive-2026-10-12.json). The first attempt stopped at the disk-reserve check with originals untouched; the successful bounded retry used a 10 GiB reserve with approximately 17 GiB available locally and 294 GiB externally. The empty first-attempt staging directories were retained.

Both strict and catalog-only workspace layout checks passed. Raw archive contents remain private and are not committed.
