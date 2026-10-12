# ACE workspace migration report

Observation date: October 10, 2026. Scope: the named local workspace, its direct source repositories and linked worktrees, the 15-project ACE Page catalog, and five resolved source-owner references.

This is the historical 1.0 migration record. [Migration 2.0.0](migrations/2.0.0.md)
supersedes its `system/` placement and `--workspace ..` invocation. Current checks
run as `python3 tools/workspace_layout.py check` from the coordination Git root.
The observations and preservation receipts below retain their original scope.

## Applied changes

- Established `audiovisual-composition-system` as the solution name; retained the old aggregate name as a compatibility symlink.
- Added the private `system/` coordination repository, one authored manifest, all 15 project records, repository/component/archive directories and a named editor workspace.
- Consolidated navigation through generated relative links. Source repositories, media and archive bytes remain in their original physical locations.
- Repaired eight linked Git worktrees after the enclosing folder rename. Both `git worktree repair` commands returned success; all eight linked checkouts became usable.

The worktree repair checked HEAD, complete porcelain status and tracked-diff digest before and after for both main owners and all eight linked checkouts. All matched. Main time-moment-brief retained 37 dirty entries; its detached Workspace checkout retained 20 untracked vault files. Other linked worktrees were clean.

| Linked checkout | Preserved HEAD |
| --- | --- |
| .wt-agent2-review | 60722c2dd47b839873823d545ed11d5d3bf2de0f |
| .wt-agent6-webxr | 51b57cb698f251825c0606993fa69c762e638ce4 |
| .wt-agent7-integration | 7fa91812369b5b60f09b733565c9a2507ea177ab |
| .wt-agent7-shared-engine | 2a28dd9930fce780abafd45e1f13eb161b65e945 |
| .wt-agent8-acceptance-20261010 | 4bf06b76537dd48fe71840d01b2b21c785b2afec |
| .wt-agy-choreography | 4b9b3cd34d22f458e3b2dd8b77714328b61be200 |
| Workspace/time-moment-brief | 44d815c978fc9b57526ff9b18165cd5b8d777b5c |
| .wt-agent7-simvltanea | df076d1316aae780ab2148351813840f1fbbfbe9 |

## Old to consolidated navigation

| Existing location | Consolidated access | Treatment |
| --- | --- | --- |
| audiovisual-composition-engine | audiovisual-composition-system | Relative compatibility symlink; old path resolves |
| simvltanea | projects/simvltanea/local/checkout | Same Git working tree, no copy |
| time-moment-brief | projects/time-moment-brief/local/checkout | Same private and dirty Git working tree |
| the-thing-without-a-name | projects/danse/local/checkout | Project identity normalized; source and remote retained |
| god-here | projects/god-here/local/archive | Classified as preservation, separate from postproduction implementation |
| reflect-recur | projects/nrcsvs/local/archive | Vault association preserved |
| Earlier god-here session archive | archives/god-here-sessions/local/source | Original title and bytes retained |
| temporary-work-preservation-2026-10-10 | archives/engine-recovery-2026-10-10/local/source | Recovery snapshot, not a live engine checkout |
| engine | components/spatial-audio/local/source | Staging capability, not an accepted independent engine |
| tests | components/composition-tests/local/source | Existing cross-workspace test root |

## Remaining physical migration and authority work

These items are owned by this coordination repository's migration contract until transferred to the named existing source owner. They are not claims that consolidation of source bytes has completed.

| Item | Existing owner | Acceptance predicate before mutation |
| --- | --- | --- |
| Physical checkout placement and shelf integration | Portvs workspace manifest | Explicit ACE bindings in existing workspace authority; compatible source roots, worktree paths and rollback verified |
| Shared-engine staging and source divergence | time-moment-brief shared-engine development branch and FOA source owner | Reconcile spatial-score divergence; verify pinned consumer digests and actual playback before restaging/extraction |
| Danse repository identity | Existing Danse project-record and source repository owners | Resolve private redirected origin vs distinct public personal remote; record canonical ID and rights before changing remotes |
| God-here and recovery remote custody | Existing local preservation repositories | Private remote/custody destination and exact restoration proof; source bytes remain retained meanwhile |
| Broken historical god-here README link | Existing god-here preservation repository | Replace the stale temporary-work-corpus link with a verified actual recovery index in an owner-reviewed change; no invented alias to a missing Project archive directory |
| Missing local source bindings for Page-backed works | Each project's original Page and source owner | Resolve exact implementation or archive identity and rights; add a binding, not an empty guessed repository |

Source directories are deliberately retained. The consumer resolver currently expects sibling time-moment-brief, and private/dirty source, active worktrees and repository identity discrepancies make a physical shuffle a separate compatibility migration. The new views provide one usable directory now without making that move a hidden side effect.

## Repeatability and rollback

Run `python3 tools/workspace_layout.py check --workspace ..` from system. Every expected source target must exist; every generated link must resolve to that exact source; unexpected occupied destinations fail before link creation. The generator creates no shell commands from metadata and fetches nothing.

Re-running apply creates zero links. Manifest generation is deterministic. Future manifest changes must preserve old aliases until consumers migrate.

Rollback removes only symlinks whose exact targets match the recorded mapping; it never removes a directory, source file, Git database or archive. Retain the old aggregate compatibility alias until legacy consumers and worktree pointers are independently verified. Do not use recursive deletion on navigation views.

## Evidence limits

This is directory and reference validation. No bulk transfer, source history merge, archive deletion, repository rename, public release or audiovisual reacceptance occurred. No disk recovery is claimed. The existing old editor workspace is retained as a compatibility entry.
