# Danse runtime lifecycle investigation and owner packet

Observed on the evening of 2026-10-12 America/New_York (00:35 onward on
2026-10-13 UTC). This supplements the earlier host-pressure investigation with
a distinct, measured launch-attribution cost. Raw process commands, ancestry,
open handles and source censuses remain in private custody staging under the
run ID in the [redacted receipt](evidence/danse-runtime-lifecycle-2026-10-12.json).

The first process sample contained 157 Python processes with aggregate sampled
CPU 491.7% and RSS sum 1,686,224 KiB. Eight high-CPU command samples identified
`domus-process-ownership` wrappers around MCP/native launches. Twenty-one Python
processes were parentless. Six examined parentless wrappers were subsequently
absent; this agent sent no signals and their exit cause was not captured.
A later sample recorded 140 Python processes, CPU sum 13.2%,
RSS sum 850,048 KiB and only three parentless Python processes. Summed RSS is
not unique physical-memory accounting; CPU percentages can span multiple cores.
The reduction is not claimed as cleanup performed by this agent.

Host swap fell from 89.72% to 80.39% across those observations, but admission
still denied heavy work for swap fraction and `vitals-shed`. The bounded final
settling observations are preserved in the receipt. No application restart,
signal, priority adjustment, disabled capability, config mutation, admission
override or memory purge was performed.

Danse's current source inventory and Git state were stable during a five-second
check: unchanged HEAD, 14 refs, two stash reflog entries, 4,257 ignored entries
and 1,212,543,676 logical ignored bytes. A completed open-handle probe with empty
stderr observed zero writable handles. This is a bounded observation, not an
exclusion lock against future writers. The custody runner must revalidate all
source and medium conditions if admitted.

The final settling samples still denied admission at 69.38% and 68.25% swap.
Both T7Recovery and Archive4T were absent; the APFS inventory contained neither
expected volume UUID. No alternate disk was substituted or host path created
under an absent mount. Custody remains incomplete.

## Private repository alternative

The user asked why the material cannot be committed to a private repository.
It can be preserved remotely; physical disks are one custody route, not the only
possible route. A normal source commit does not retain ignored files, stash
entries or Git reflogs. A complete private archive of Git state and material,
with checksums, remote readback and a clean restore, can provide one off-device
copy while originals remain untouched. A second independent custody destination
is still required; two repositories in one account/provider do not establish
independent failure domains by themselves.

[GitHub blocks ordinary Git files above 100 MiB](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
Larger archive objects need an appropriate mechanism such as Git LFS, with its
actual account capacity checked. The private destination, archive access and
second independent custody route remain to be resolved. The current delivery
contains redacted evidence only. Remote archival I/O must
also respect admission rather than bypassing the pressure gate.

## Concrete ownership and repair boundary

The managed `domus-process-ownership` launcher in **domus-genoma** starts its
native child and then synchronously invokes `module.observe(Path.cwd(), "")`
for attribution before waiting for child exit. The inspected **Limen** workspace
implementation of `process_ownership.snapshot` enumerates the process table,
collects all process working directories and reads identities/native details
for user processes. Per-launch full observation can amplify concurrent startup
cost. This is a source-derived explanation consistent with the measured wrapper
CPU; the exact immutable runtime module of every sampled worker was not pinned,
so it is not presented as a verified runtime defect or a deployed repair.

The launcher explicitly states that observation never adopts or signals jobs.
The inspected `mcp_process_custody.Custody` only releases process groups created
by its own probe; it cannot safely adopt arbitrary already-running helper fleets.
No supported local API for releasing another desktop connection's inactive MCP
fleet was established. A live parent or service endpoint is not abandonment.

Next source-owner action: Domus and Limen runtime owners should pin the active
immutable protocol release, measure launch attribution against that exact code,
then review a child-specific, identity-bound observation path with an explicit
deadline. Retain shared-service attribution and visible unmeasured outcomes;
do not disable ownership verification or silently skip a declared capability.
This is an owner repair packet, not authorization to rewrite deployed config or
patch a running vendor bundle.

Acceptance: concurrent native MCP launches retain correct child identity and
service attribution, bound observer CPU/time and observer descendants, exit via
normal lifecycle, and preserve active peer tasks. The desktop runtime owner
must also establish a supported inactive-fleet release boundary. Once real host
admission clears, the existing custody runner can secure the current checkout;
only verified copies and a clean restore can close that custody step.
