# Danse custody: conditional pressure and writer recheck

User authorization: recheck host pressure and source writers; complete both
private copies and a clean restore only if admission clears and inventory is
stable. Preserve originals, push redacted evidence, leave both PRs open.

1. Read fresh host admission status; do not acquire or copy under a denial.
2. Inspect open handles with a bounded lsof probe, retaining raw output privately.
   Compare complete metadata censuses and Git state across a five-second window.
3. If both conditions pass, run the existing bounded full-store custody runner
   with fresh acquisition, independent-media proofs and drift rejection.
4. Otherwise retain private census evidence, commit/push the redacted recheck
   and stop this attempt without retrying unchanged pressure.

Outcome: host status at 2026-10-12 20:21 UTC remained denied for swap fraction,
disk throughput and vitals shed. Metadata and Git state were stable in the
bounded observation. No heavy acquire, payload hash, copy or restore began.
See docs/evidence/danse-private-custody-recheck-2026-10-12.json. Existing copies
and restore remain unverified; all original source state and partials retained.
