# Danse source authority and custody reconciliation

Observed on 2026-10-12. Repository authority is resolved: the canonical Danse
source is private GitHub repository **1320324017**, currently named
`4444J99/the-thing-without-a-name-screendance`. The native project's declared
`organvm/the-thing-without-a-name` URL is a retained redirect to that same
repository. Its stable native identity remains `project_id: danse`.

The configured `personal` remote is a different repository, **1347780050**,
`4444J99/the-thing-without-a-name`. It is public and archived. Its
[merged archival PR #13](https://github.com/4444J99/the-thing-without-a-name/pull/13)
and [README at its exact main commit](https://github.com/4444J99/the-thing-without-a-name/blob/2e105c30b69033fa665cfcaacff4c393f94dada3/README.md)
explicitly designate the legacy canonical URL and classify the public repository
as a retained, non-authoritative continuation. This agrees with the local
`project-record.yml`, `LINEAGE.json` and agent contract. A redirected name and
an archived continuation therefore do not establish competing current authorities.

## Identity and lineage evidence

| Surface | Observed identity | Disposition |
| --- | --- | --- |
| Local `origin`, fetch and push | Legacy canonical URL; live API resolves ID 1320324017 | Retain unchanged; private canonical source |
| Private canonical `main` | `73da6dc1c4339c9cc75c8253c7ef5173e4091256` | Live GitHub and advertised Git refs agree |
| Local Danse `main` | `f6f27c10a4bf617d895b0f0387eb3013aa39913b` | Four commits ahead of canonical main, zero behind |
| Local `personal`, fetch and push | Public archived ID 1347780050 | Retain historical remote unchanged |
| Archived public `main` | `2e105c30b69033fa665cfcaacff4c393f94dada3` | Archival PR #13; not a backup of current private source |

The public and private main histories share merge base
`e6dac59730f612a9f6ab035b615c3be6d179aac4`. The public head is not an ancestor
of local main: its one unique commit changes README.md to the archival notice.
Local main has 63 commits absent from that public branch. The archival notice's
disposition is authoritative evidence; it does not make the divergent tips
byte-identical or authorize merging either history into the other.

The [machine-readable receipt](evidence/danse-source-authority-2026-10-12.json)
pins repository IDs, heads, local source-document hashes and live advertised-ref
reachability. Source Git stores were read without fetching or updating their refs.
GitHub's cross-repository compare endpoint returned 404; ancestry and counts were
instead computed from the already-present exact local commit objects.

## Custody reconciliation

Authority resolution does not close preservation. The canonical private remote
advertises the ambisonic feature head and archive tag, but these retained local
refs are not reachable from any of its advertised heads or tags:

| Local ref | Unreachable commit count | Next owner action |
| --- | --- | --- |
| `main` | 1 | Review the retained merge commit through the native source delivery process |
| `topic/engine-extraction-integration` | 2 | Preserve and disposition the exact topic delta through its source owner |
| `refs/stash` | 4 | Preserve the stash in private custody before any explicit disposition |

Counts are per-ref reachability and may overlap; they must not be summed.
Although main is four commits ahead of remote main, its three feature commits
already exist on the advertised feature branch. Only its merge commit remains
unreachable from the complete advertised private head/tag set.

The earlier local checkout census recorded **165 ignored regular files / 934,334,052
logical bytes**, with zero symlinks or stat errors in that bounded metadata pass.
The subsequent [private custody preflight](danse-private-custody.md) supersedes
that count with a recursive, changing inventory and records the denied heavy
acquire. It does not establish completed custody.
No filenames or private contents are copied into this report. This is a census
of this checkout's ignored files, not a complete Danse archive census, digest
inventory, independent copy, or restore proof. `assets/lock.v1.json` is absent.
The existing asset documentation defines 487 production inputs; the availability
rail and its schema do not demonstrate that those inputs are hydrated or secured.

The native [custody issue #21](https://github.com/4444J99/the-thing-without-a-name-screendance/issues/21)
is open. Its contract requires complete checksums, two independent copies,
a clean restore, a redacted receipt and explicit disposition. The source's
2026-08-04 v2 receipt remains historical evidence of two blocked material roots;
its earlier size figures are not current measurements. This pass does not
rediscover those former worktrees or upgrade that receipt to successful custody.

The system's six-file T7Recovery receipt covers TMB derivatives and screenshots,
not Danse. The separate Ingress plan covers TMB and backwards-up-hill originals.
Neither can be reused as Danse copy or restore evidence.

## Remaining work and boundaries

1. The native source owner reviews the unpublished merge/topic deltas and retains
   the stash. No private source is pushed to the archived public remote.
2. The custody owner locates every retained historical and current Danse material
   root, then issues a fresh complete private checksum inventory. Include Git
   refs/stashes, ignored material and any required LFS/reflog/unreachable-object
   coverage; advertised-ref checks alone are insufficient.
3. Under fresh admission and exclusive I/O ownership, review and use the full-store
   custody runner described in [the custody checkpoint](danse-private-custody.md).
   The native HEAD-only snapshot and remote-equality predicate do not cover this
   preservation scope. The runner preserves the complete standalone Git store
   and both stash reflog entries without changing source publication parity.
   The current heavy acquire is denied; no copies or restore are verified.
4. Verify both copies and a clean restore, publish only the redacted receipt,
   and retain originals. Publication rights, final release, physical acceptance
   and any future reclamation remain separate source-owner decisions.

Only the coordination manifest, generated views and explanatory evidence change.
The original source URLs remain usable aliases. Repository authority is resolved;
source publication parity and independent Danse custody remain incomplete.
