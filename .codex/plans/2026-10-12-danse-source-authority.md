# Danse source authority and custody reconciliation

Scope: reconcile existing Danse identities and custody evidence in coordination
metadata. Preserve every source checkout, ref, stash, remote and media file.
PRs #2 and #3 remain open and unmerged. Use an isolated coordination worktree
because another task is writing in the original coordination checkout.

1. Read the native project record, lineage, archival disposition and custody contract.
2. Resolve both configured remotes against live numeric GitHub IDs and exact main heads.
3. Compare existing local objects and advertised refs without fetching into sources.
   Inventory ignored material by metadata only; distinguish it from verified custody.
4. Record the canonical redirect, archived continuation, publication gaps and
   custody prerequisites. Update the solution manifest and regenerate its views.
5. Run catalog and scoped safety checks, verify unchanged source snapshots,
   commit explicit coordination paths and push the follow-up to existing PR #3.
6. Retain both coordination checkouts. No source publication, bulk transfer,
   extraction, remote rewrite, history merge, cleanup or media acceptance is included.
