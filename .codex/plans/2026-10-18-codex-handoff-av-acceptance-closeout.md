# Handoff to Codex: audiovisual acceptance and session closeout

Written 2026-10-18 02:25 EDT by Antigravity. Status is evidence-bound: nothing below is merged, live, or accepted unless it says so. Prior "PASS/COMPLETE" dashboard labels were withdrawn after external audit. Treat all recalled paths and SHAs as hypotheses; re-verify against disk and git.

## Why this handoff exists

The Antigravity teamwork run (sentinel, orchestrator, workers) and the parallel DeepCoder stopped on a provider quota (429, resets about 05:22 EDT). Remaining work needs one owning writer per checkout. Codex is that owner.

## Three independent finish lines (none met)

1. Playback works as specified (production player and panoramic proof, judged separately).
2. Originals have verified custody and restoration.
3. The session has a valid release receipt for the ORIGINAL session.

Do not use a weighted completion percentage. Filing a failure is not resolving it.

## What is durably homed now

| Item | Location | SHA | State |
|---|---|---|---|
| Custody plan v2 + inventory/reconciliation/Take 48 evidence | `audiovisual-composition-system`, branch `docs/god-here-touchdesigner-source-20261013` | `cf3cb36` | pushed; docs/JSON only; not merged |
| TMB WIP checkpoint (playback, proof, packaging guards, gate files) | `time-moment-brief`, branch `feat/n-generation-soak-harness` | `ce28cf2` | pushed; NOT ACCEPTED; not merged |
| Limen producer repairs | PR #2988, branch `feat/session-closeout-receipt-producer` | `a58b04a80` | pushed; OPEN; not merged |

Untracked files in `audiovisual-composition-system` (`Backup/`, `Log/`, `*.toe`, `tools/inspect_touchdesigner_session.py`) belong to other work. Do not touch or commit them.

## Remaining work, in order

### A. TMB repairs (one writer; branch above)
Open defects found by review although 14 gates exit 0:
1. `package_audio.py` can overwrite an existing file when `ffprobe` fails.
2. The audio manifest can be written unconditionally.
3. `scripts/verify.py` can select `HEAD~1` and miss earlier branch changes; use the live default-branch merge-base.
4. The `tmb-packaging-guards` gate is `py_compile` only; add real overwrite-prevention tests.
5. Hiding the proof page can leave audio advancing; suspend the audio context on hide and resume on show.
Also: two reviewers (`reviewer_m2_2` and one other) requested changes; natural-loop and per-generation-seek evidence is weak. Add tests for at least three births, three natural wraps, later-generation navigation, eviction return, distinct seek phases, non-loop-aligned pause/resume, and promotion with no audio source reset. Keep limits: workers/decoders <= 12, queue <= 256, bitmaps <= 12, textures <= 24, frame step <= 1, A/V offset <= 50 ms.
Soak harness `tests/e2e/soak_n_generation.py` still patches playback, forces seeks and advances transport; remove that from acceptance runs, make failed or insufficient measurements exit nonzero, and drop the unexplained +/-5% allowance in favor of the transport equation tested against an independent clock with explicit pause, buffering and uncertainty terms. Guard legacy packaging before any write so real-source acceptance evidence cannot be overwritten.

### B. Limen PR #2988 (one writer; branch above)
1. Re-verify at the current head with the scoped resolver, not historical totals.
2. Confirm the auditor's gap is closed: complete implicated-gate coverage, attestation bound to exact base, head, changed-path digest, registry/resolver fingerprints, selected gates and terminal results, v2 receipt shape unchanged.
3. Confirm: structural manifest gaps block final check and head rechecks; custody absence rechecked at release; fork-point inputs verified against the live default-branch tip; surviving predicate descendants rejected; 8 MiB output ceiling; create-only writes clean up partial files; `plan` and `check` stay read-only.
4. Disposition every review finding (accept, reject with rationale, defer, supersede). Land only through limen's registered merge rail (`scripts/merge-policy.sh` CLEARED, bounded fix-on-review). Then verify merged ancestry, installed adoption, and runtime behavior as three separate claims.
5. Mind the writer lease (`scripts/host-work-admission.py status --no-probe`) before creating a worktree.

### C. Sustained measurements (after A)
Approved 65-minute window, one workload at a time: 1800 s Chromium/Metal soak, then 600 s Safari proxy, then 600 s Safari full, harness wrapping disabled. A failed prerequisite stops the sequence. Safari permission changes stay operator-controlled. Report buffering holds separately. Run scoped checks once per changed tree.

### D. Original-media custody
Preserved facts (verify): two roots `backwards-up-hill` and `time-moment-brief`, with `palm-beach-christmas` and `pompano-concepts` as TMB source collections; the 347-path/281.53 GB historical inventory includes Finder metadata and is not a count of recordings; six loose Ingress candidates were hashed in place; Take 48 is the only found common-coverage window, so keep "four views / three sensors".
Not done: no independent copy, no completed restore. Ingress and Archive4T share one physical store; T7Recovery is disconnected. Required: reconfirm stores by UUID, ownership, capacity, metadata overhead and a 20 GiB reserve; stream hashes; copy without overwrite; reopen and verify destinations; complete restore with exact membership, hash and metadata checks; preserve interrupted files and ledgers. Admit bulk copying only within measured capacity, throughput and remaining allowance; stage under `$LIMEN_CUSTODY_STAGING_ROOT` (mode 0700), never in a vendor runtime root. Exhaustion produces a checkpoint, not a completion claim. Preserve all originals; no deletion.
Search BUH clips, chapters and audio anchors for genuine common four-camera coverage before proposing capture; another interval is an alternative family, not a repair of the original passage. Matched MAX video/FOA acceptance is separate from the fourth-camera requirement. Phone, headset, loopback and independent-disk availability remain pending. Preserve the declined history purge.

### E. Session closeout (evidence recovery, not a new-session demo)
Recover the ORIGINAL session's authentic native identity and `/Users/4jp` anchor. The legacy transcript reader expects Codex-style metadata while the report references a Claude session, so an identifier alone may not suffice. Preserve its full repository scope; never substitute this session, a child checkout, or a fabricated transcript. If authentic evidence cannot establish release, record that exact limitation; a new-session demonstration cannot release the old one. Resolve the blocked workspace-scope discovery through its owning admission mechanism and do not repeat unchanged denied commands. Then produce and publish the scope-bound owner receipt and require two bare closeout checks returning 0 with no second-run side effects. A valid handoff may release a session while custody and physical acceptance remain unfinished, but full task completion requires both.

## Rules to carry
- Inspect worktrees, branch state and claims before mutating; no two writers on one checkout or branch. Preserve dirty and concurrently owned checkouts.
- Reclaim a checkout only with positive landing, ownership and custody proof.
- No force-push to main; no direct push to main; no code-amend in response to review comments.
- Guard escalation: after two identical denials write one script and hand over dry-run and apply commands.
- Resume budget: at most two implementation tasks and one heavy workload; 30-minute attempts including at most 10 minutes of verification.
