# Audiovisual Composition System

The coordination repository for all 15 projects in ACE. It owns project membership, names, repository relationships, directory views and the migration contract. Existing repositories own their implementations; archives retain their original bytes.

Start with [the directory design](docs/directory-architecture.md), [the complete project catalog](docs/project-catalog.md), and [the migration report](docs/workspace-migration-report.md).

`workspace-manifest.json` is the sole authored membership and binding source for this solution. Generated project READMEs and the editor workspace are views. Project IDs reuse the observed ChatGPT identities; Danse also retains its existing `project_id: danse`. The manifest is solution membership, not a replacement for the estate registry or each repository's native metadata.

## Use

From this repository:

```sh
python3 tools/workspace_layout.py check
python3 tools/workspace_layout.py apply --workspace ..
python3 tools/workspace_layout.py check --workspace ..
```

`apply` only creates missing directories and relative symbolic links after checking all planned destinations for collisions. It does not move or delete source files, fetch media, execute manifest content, rewrite Git history, or modify another repository. Re-running it is idempotent.

The enclosing workspace remains non-Git. Its `projects/`, `repositories/`, `components/` and `archives/` paths are consolidated navigation views. Physical legacy locations are retained for working consumers. See the migration report for the exact deferred relocation predicates.

This repository is private because solution membership includes private works and source relationships. No media, chat transcripts, recovered binaries or private derivatives belong here. EES informed the design; this is not a claim of EES certification or audiovisual acceptance.
