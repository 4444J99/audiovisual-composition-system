# Danse private custody checkpoint

**Custody remains incomplete.** The fresh heavy acquire at 2026-10-12 19:54 UTC
was denied for `swap-fraction`, `disk-throughput` and `vitals-shed`: swap was
60.76%, growing by 313,289,374 bytes/minute, with sampled disk throughput
168.09 and 216.04 MiB/s. No source payload was hashed or copied. There are zero
verified copies and no verified clean restore. Originals and both PRs remain
retained for review.

The [final redacted preflight receipt](evidence/danse-private-custody-2026-10-12-v3.json)
records source HEAD `f6f27c10a4bf617d895b0f0387eb3013aa39913b`, 14 refs and **two
stash reflog entries**. Git state and the metadata census were unchanged during
that bounded preflight. This comparison is not a source-content checksum proof.

The earlier 165-file figure is superseded for this current checkout scope.
Recursive metadata passes found 965 ignored entries / 965,462,667 logical bytes
at 19:53 UTC, then **4,256 ignored entries / 1,209,577,527 logical bytes** at
19:54 UTC. The changing inventory must be quiescent for a successful custody
run. The runner includes all ignored material, including environments and caches;
it does not reduce the scope to force agreement with 165. Its final full-tree
preflight covered 5,317 file/link entries / 1,374,544,418 logical bytes including
the complete Git store. Literal link targets are preserved without following
them. These figures are time-bounded observations, not a frozen current total.

T7Recovery and Archive4T passed Danse's native physical-medium independence
check, and both destinations plus local restore staging passed capacity checks
with a 20 GiB reserve. Passing these checks is not evidence that copies exist.
Private preflight manifests and full receipts are retained under mode-0700
`$LIMEN_CUSTODY_STAGING_ROOT` (the default Limen private custody staging root),
keyed by the run IDs in the redacted receipts. They contain filenames, exact
refs, remotes and metadata; those private manifests are not published here.

## Preservation path

The native `scripts/private_custody.py` snapshot requires remote parity and
bundles HEAD only. Local main is ahead of its private remote, and a HEAD-only
bundle cannot secure other branches or older stash reflog entries. The new
coordination runner [tools/custody_danse.py](../tools/custody_danse.py) preserves
the entire standalone checkout and `.git` store instead. It reuses the native
physical-medium proof without changing that tool or pretending remote parity.
It refuses shallow stores, alternates, submodules, external core.worktree
configuration, Git lockfiles and special filesystem nodes.

An admitted run would copy source to a unique private T7Recovery root, read back
and compare its checksums and metadata, then copy to a unique Archive4T root and
verify again. A third fresh directory in local private staging is restored from
the second copy. Exact Git state, stash reflogs, tracked cleanliness and full
Git fsck are checked there. All source names and originals stay in place. Every
incomplete run and partial copy is retained; no archive is published to GitHub.
The two independent copies need distinct physical disks; the clean restore
needs a fresh directory, not a third independent disk.

Four local fixture checks pass: literal links are not followed, special nodes
are rejected, public-permission custody parents are refused, and a full-store
fixture copy retains a local-only branch, two stash entries and ignored bytes
with matching hashes/metadata and passing Git fsck. These checks do not validate
an admitted real Danse transfer or establish its custody.

The catalog check and scoped Gitleaks scan also pass. The full workstation layout
check in the retained isolated review worktree cannot pass because the declared
Earlier god-here session archive is absent there. No source directory was moved
or fabricated to clear that check; the catalog-only check validates the generated
contract without claiming workstation source availability.

Two preliminary preflights are retained as
[v1](evidence/danse-private-custody-2026-10-12.json) and
[v2](evidence/danse-private-custody-2026-10-12-v2.json). V1 refused literal links
before completing a census; its `source_preserved: false` means preservation
could not be verified by that incomplete census, not that files were changed.
V2 unnecessarily required the restore staging root to pass third-medium proof;
the internal system volume failed that proof. The corrected final preflight
passed the actual two-medium requirement and reached admission. No preliminary
pass copied payload or changed source state.

## Next bounded run

After host pressure materially changes and source writers finish, start one
fresh, admitted attempt with a new receipt filename:

```sh
python3 -B tools/custody_danse.py --source /Users/4jp/Workspace/audiovisual-composition-system/the-thing-without-a-name --redacted-receipt docs/evidence/danse-private-custody-next.json --wall-seconds 1200
```

Do not retry the unchanged denial or override pressure policy. The runner also
supports `--preflight-only`, which can never report completed custody. Commit
the next redacted receipt only after inspecting it and running scoped checks.
This covers the current checkout, not the undiscovered historical material
roots in Danse's August receipt or the absent 487-input production asset lock.
The native [custody issue #21](https://github.com/4444J99/the-thing-without-a-name-screendance/issues/21)
remains unresolved; source publication parity and any later reclamation require
their own evidence.
