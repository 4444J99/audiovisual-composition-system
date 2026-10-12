# Workspace Layout 2.0

Implement the supplied plan on distill/phase-1, preserving source paths, remotes, histories, dirty work and original archival filenames. Commit locally; do not push before user review.

1. Snapshot all five source Git repositories before changes.
2. Version the manifest and root allowlist, restore generated views, generate source ignores, implement strict local checks and read-only status, retain collision-safe links.
3. Update CI, safety tests, architecture and versioned migration evidence.
4. Run Python and Node tests, local checks, isolated clean-checkout CI check, deterministic render and before/after source comparison.
5. Review explicit staged files, commit on distill/phase-1; retain this checkout.

Inspection adjustments: the old empty backwards-up-hill source directory is absent; record the unresolved binding rather than creating source material. Four loose legacy Markdown files remain declared and ignored. CI uses explicit catalog-only validation because workstation sources are not distributed with the coordination checkout.
