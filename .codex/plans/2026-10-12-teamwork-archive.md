# Archive stale teamwork state

Scope: only `.agents/teamwork/`. Preserve historical instruction files as private records; leave other agent state and all active source checkouts untouched.

1. Check open handles, process path references, nested repository state and source stability.
2. Inventory and encrypt an external snapshot using the existing independently escrowed backup key.
3. Read back, decrypt and extract the external snapshot; compare every path, file digest and ordinary metadata field. Preserve original extended attributes separately.
4. Recheck activity and source stability, then move the original tree intact into private custody staging.
5. Publish a sanitized recovery receipt and verify the workspace layout.

Recovery evidence: `docs/evidence/teamwork-archive-2026-10-12.json`. The private archive contains restoration instructions. This is preservation, not product acceptance or disk-space recovery.
