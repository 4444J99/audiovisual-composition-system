# Audiovisual Composition System

The coordination repository for all 15 projects in ACE. It owns project membership, names, repository relationships, directory views and the migration contract. Existing repositories own their implementations; archives retain their original bytes.

See the [functional identity rollout and validation](docs/functional-identity-rollout.md).

Start with [the directory design](docs/directory-architecture.md), [the complete project catalog](docs/project-catalog.md), and [the migration report](docs/workspace-migration-report.md).

The [TMB spatial composition report](docs/tmb-spatial-integration-report.md) records
the verified integration, source identities and reproducible local preview.

`workspace-manifest.json` is the sole authored membership and binding source for this solution. Generated project READMEs and the editor workspace are views. Project IDs reuse the observed ChatGPT identities; Danse also retains its existing `project_id: danse`. The manifest is solution membership, not a replacement for the estate registry or each repository's native metadata.

## Use

From this repository:

```sh
python3 tools/workspace_layout.py check
python3 tools/workspace_layout.py apply
python3 tools/workspace_layout.py status
python3 -m unittest discover -s tools/tests -v
node --test tools/tests/test_verify_tmb_composition.cjs
```

`apply` only creates missing directories and relative symbolic links after checking all planned destinations for collisions. It does not move or delete source files, fetch media, execute manifest content, rewrite Git history, or modify another repository. Re-running it is idempotent.

CI uses `check --catalog-only` because ignored workstation sources are absent from a clean checkout. Local `check` additionally requires every declared source and navigation link. `status` reads local Git state and cached upstream ahead/behind counts without fetching. CI runs the manifest, generated-directory, preservation and acceptance-guard
checks on every pull request and main-branch push. Workstation links and real
private-media playback are verified locally. Directory names and records are
enforced by the same manifest validator in both environments.

This repository is the workspace root (schema 2.1.0). Its `projects/`, `repositories/`, `components/` and `archives/` paths are consolidated navigation views. Physical legacy locations are retained for working consumers. See [migration 2.0.0](docs/migrations/2.0.0.md) for placement, consumer evidence and rollback. Every top-level entry is declared; source folders and preserved loose files are ignored through a deterministic generated block.

Authenticated GitHub metadata reports this repository as **public** (verified 2026-10-13). Earlier claims that it was private were incorrect. Generated views omit private implementation relationships and local/Page metadata; new private source bindings are rejected. Existing published history has not been retracted. No media, chat transcripts, recovered binaries or private derivatives belong here. See the [functional identity contract](docs/naming-responsibility-contract.md) and [migration 2.1.0](docs/migrations/2.1.0.md). EES informed the design; this is not a claim of EES certification or audiovisual acceptance.
