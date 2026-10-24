# Audiovisual Portfolio Gap Closure and Build Evolution Implementation Plan

> For agentic workers: execute bounded tasks through the existing project owners, using superpowers:executing-plans or superpowers:subagent-driven-development when that execution route is admitted. Checkboxes record observed completion only. This document is planning, not a production acceptance receipt.

**Goal:** Complete the remaining audiovisual portfolio work, establish a practical drive-independent working set and independently restorable media custody, and release accepted editions through their existing owners.

**Architecture:** Keep ACE as the coordination and identity layer. Extend the existing playback, loop-composition, postproduction, timed-text, deterministic-performance and historical-web implementations. Each artwork owns its composition and edition; each implementation owns its executable contracts and evidence. Private media, locators and native operational receipts remain private.

**Tech stack:** Existing Python/amp CLI, JavaScript/browser and Web Audio runtimes, TouchDesigner, FFmpeg/native media tools, Photos intake, Git/GitHub and existing manifest/custody tooling. Pin each owner's current lockfiles and runtime versions; this plan introduces no platform replacement.

**Spec:** User directive on 2026-10-24: plan all gap closure and remaining next moves, critique the current build and include its improvements. This extends the retained October 22 portfolio scope and October 23 first-packets plan, [functional identity contract](../../docs/naming-responsibility-contract.md), [composition evidence lifecycle](../../docs/composition-evidence-lifecycle.md), and [God's Ears master program](https://github.com/4444J99/audiovisual-media-postproduction-system/issues/63).

**Status:** Plan only. No checkbox below is an implementation, media-transfer, deployment, artistic-acceptance or release claim. The native execution hold remains owned by [ACE #12](https://github.com/4444J99/audiovisual-composition-system/issues/12). Documentation publication does not change that hold.

**Owner:** ACE coordination for this plan; source owners in workspace-manifest.json for implementation; existing private custody owner for media and source locators. Human artistic selection and distribution decisions remain attached to their exact editions. Existing task/issue IDs remain authoritative.

**Date:** 2026-10-24 UTC. Planning baseline below was checked on this date. Execution refreshes only the relevant changed inputs and exact head.

## Context and baseline

| Owner / scope | Inspected state | Planning consequence |
| --- | --- | --- |
| ACE coordination | Main a9f75256147e89a785fb6d9ed6fa496583f1e4e8; 15 project records; 13 artwork records; six implementation owners. Existing local coordination branch contains unrelated native files. | Preserve identities and isolated ownership; do not turn project count into artwork/release count. |
| Timed-text navigation | Main 068ef112f0ec624549b065d0ce72981cc20121b7; historical edition hosted; experimental PRs 59/61/62/63 merged. | Verify the newer edition and its artistic selection; do not describe the historical site as unreleased. |
| Shared playback / time-moment-brief (TMB) | Exact main/WIP refs remain in its private owner crosswalk. Main records resource/frame/A-V failures. Draft still drives boundaries and exits zero on completion irrespective of verdict. | Repair observer truthfulness, then measure natural production behavior. |
| Independent-loop compositor | Main a8ff62745c08fec8e66e38f8f8a0fe39a18c3eee; 2-7-loop/audio/export capabilities and accepted importer exist. | Finish one actual edition; independent functionality need not wait for complete TMB scheduler acceptance. |
| Postproduction | Main 664a47aca1f68d84c3dd5440363b1a48ba32243f; native work on draft PR 62; master 63 retains 53 tasks / 38 deliverables plus older obligations. | Reconcile current native/Studio/source states; finish both authored and generative scopes. |
| Historical multimedia | Main 4dbbcd77ce410645382f8903558aa3756c4df91d; catalogue 143 and publication pipeline 145 merged; navigation 138 and offline 182 open; publication-needs remains blocked. | Reuse landed work; finish actual runtime and publication predicates. |
| Deterministic performance / Danse | Canonical private owner resolved; retained local work and open changes remain to reconcile through its private owner crosswalk. | Preserve private source authority; repeatable input hydration, audio/capture and reopening remain required. |
| Media custody | Full recorded source set about 292.34 GB; internal free capacity about 100.9 GB. Source and newer archive copy share a physical SSD. Separate recovery SSD has about 30.2 GB free. | Full source migration to the laptop or current recovery SSD is not viable. Independent full custody remains open. |
| Native working material | Base God-here catalog has 228 entries and recovered-room catalog 56 more. Some entries contain image sequences. TMB has 16 local derivatives totaling 32,142,002 bytes. | Asset presence is useful evidence, not dependency closure. Earlier 342 MB God-here figure counted direct files only and is not a complete working-set measurement. |

Short SHAs above are discovery anchors; execution must resolve full SHA and current relationship to accepted/default and retained WIP heads. Do not promote old measurements into current passes.

## Global constraints

- Audiovisual work only. No general laptop cleanup, unrelated backlog or repository consolidation.
- Preserve original media, source text, filenames, history, untracked/native work and private source boundaries. No deletion, drive formatting, ejection or visibility change is authorized by this plan.
- Every change uses an exclusively owned topic branch/checkout or the owning documented publication route. Existing active checkouts remain retained. Check claims and writer/heavy admission before mutation.
- At most two implementation lanes and one heavy workload; one recovery writer while recovery containment applies. Each ordinary attempt is at most 30 minutes, including at most 10 minutes verification; 120 cumulative agent-minutes per approved outcome across descendants/restarts. One corrective retry requires changed inputs. A longer media measurement requires its own valid allowance.
- New external-service and generation spending remains USD 0. Model access, hardware, terms and input eligibility are verified at execution. No new external footage upload is implied.
- No weakened measurements, hidden capability removal, dummy media substituted for real acceptance, relabelled method fallbacks or manufactured green states.
- Keep available, implemented, technically verified, perceptually reviewed, artistically accepted and published evidence separate. Reuse existing task-state vocabulary; these are evidence fields, not new task statuses.
- Raw media/source paths, private implementation bindings, model weights, fonts, keys, native state and private reviews never enter this public plan or public fixtures.
- Keep existing plans immutable. This plan adds scope reconciliation; it does not retroactively mark or erase their unfinished work.
- Every packet ends in a pushed owner commit/PR, an exact evidence receipt, or an explicit blocker in its existing owner. Only the human closes permanent atoms.

## Design choices and critique

The recommended approach is to evolve the current implementations around complete, source-bound editions. A portfolio-wide engine rewrite would defer finished work and duplicate existing responsibilities. A release-only push would leave portability, measurement and restoration gaps. The selected approach combines shared repairs with independent edition delivery; the recommendation is the planner's design judgment.

| ID | Observed weakness or design risk | Improvement and disposition | Owning task |
| --- | --- | --- | --- |
| C01 | Work rotation, software availability and artwork release can be conflated. | Accept: derive one readable project/edition view from the existing manifest and source evidence, with separate dimensions and exact pins. | T01, T14 |
| C02 | Membership/source bindings remain incomplete for several Page-backed works. | Accept: recover named sources, retain explicit missing records, resolve owners by evidence, and prevent new orphan implementation trees. | T01, T12 |
| C03 | Manifest control characters can create additional ignore directives; ACE #13 owns the reproduced defect. | Accept: reject controls before path construction and preserve current valid generated output. | T02 |
| C04 | Local catalog presence omits frame-sequence contents, code, fonts, native tables and external runtime dependencies. | Accept: dependency-closed working sets, portable private resolution and actual drive-unavailable acceptance. | T03 |
| C05 | Matching archive copies on one SSD are mistaken for independent custody; current runner cannot ingest every source form. | Accept: explicit physical-target validation, complete inventories, resumable independent readback and restoration. | T04 |
| C06 | TMB acceptance drives boundaries and can return success for failed/insufficient verdicts. | Accept: independent observers, truthful exits and separately labelled diagnostic trials. | T05 |
| C07 | Several older TMB repair requests are already implemented in retained WIP. | Supersede rebuild proposals: verify packaging guards, merge-base selection and hidden-page audio suspension at current exact head. | T05 |
| C08 | SIMVLTANEA eagerly materializes assets, accumulates events and has limited cancellation/interruption/disposal behavior in inspected source. | Accept as source-observed limits: reproduce relevant cases, add bounded lifecycle recovery, then an authenticated paged resolver for remote albums. | T07 |
| C09 | Technical catalogs/branches outpace integrated historical-web runtime evidence. | Accept: reconcile navigation, cache and publishing changes, then observe a real end-to-end journey. | T08 |
| C10 | Native/Studio state and speech/reconstruction qualification can be mistaken for accepted materials. | Accept: preserve native work, qualify language/sound/picture and use the same material/performance contracts across supported surfaces. | T10, T11 |
| C11 | More controls and techniques can increase friction without improving composition. | Accept as a design proposal: retain Review/Compare/Compose/Library/Project, expose intent and reversible comparison first, and independently control density, simultaneity, vocabulary, temporal depth and intelligibility. | T10, T11, T13 |
| C12 | A first passage could silently replace the full authored film, nine-method program, generative instrument or reconstruction. | Reject scope reduction: retain every existing deliverable and cross-map reuse without closing unmet obligations. | T11, T14 |
| C13 | Missing rights, human selection or device evidence could be treated as a universal stop or silently waived. | Accept: constrain only affected edition/capability and keep an actionable owner and evidence requirement. | T01, T14 |
| C14 | Postproduction shot boundaries accept non-finite values, allowing silent selection failure; issue 117 owns the defect. | Accept: validate finite numeric boundaries before composition admission and preserve ordered-shot positives. | T10 |
| C15 | Photos staging defaults can create links or replace existing outputs; dry-run can still scan the whole library. | Accept: bounded metadata census, explicit copy mode and fresh canonical output roots; add no-clobber/resume guards for active staging. | T07 |

Existing good foundations to preserve: functional identities separated from artworks; immutable source addressing; independently clocked loops; no-clobber edition publication; historical source bytes; saved native studies; CLI-first postproduction; full-frame reference; explicit qualification and existing bounded evidence lifecycle.

## Review focus

1. Missing drive, relocated working directory, missing font or partial sequence must produce a named dependency failure before work can overwrite saved state. T03.
2. Interrupted copy, restored receipt or same-device destination must never produce a complete-custody claim. T04.
3. Finished process with FAIL/INSUFFICIENT, manufactured wraps or same-clock expected/actual values must never pass playback acceptance. T05.
4. Hidden page, cancelled start, audio interruption, orientation change or reload must preserve recoverable state, bounded resources and explicit audio behavior. T06/T07/T13.
5. A generated image/word/voice, substitute model or partial repertoire must never acquire source-truth, method-equivalence or full-scope acceptance by omission. Non-finite composition boundaries must fail admission. T10/T11/T14.

## Order and outputs

Work order is dependency-driven. Public release order is evidence-driven.

```text
T00 admission/ownership -> T01 coverage + T02 path boundary
                                  |
               +------------------+--------------------+
               |                  |                    |
        T03 portable kits     T05 TMB observer    T06 hole-loop
               |                  |                    |
        offline work proof    natural playback     release candidate 1
               |
        T07 SIMVLTANEA lifecycle + actual edition -> candidate 2

T04 independent custody ------------------------------> restore proof
T08 historical web -> OGOD / mavsoleum-a / etc --------> conditional next wave
T09 Danse + T10 native basis + T12 source studies ------> accepted packets
T11 full God's Ears program + T13 operator refinement -> full editions/instrument
T14 source-owner acceptance -> publication -> clean replay -> retained closeout
```

T04 can continue alongside production only within the single heavy-workload allowance. Failure of a TMB-specific scheduler predicate does not block independently verified artwork behavior. No fixed release dates are promised before the required evidence exists.

## Complete project-to-task coverage

| Manifest project | Owner/work class | Full completion path in this plan |
| --- | --- | --- |
| time-moment-brief | Shared playback software | T03 -> T05 -> T14: portable inputs, truthful observer, natural playback, consumer acceptance. |
| hole-loop | Timed-text artwork | T06 -> T13 -> T14: C1 acceptance, selected C2 edition, retained C3-C6 conditional roadmap. |
| simvltanea | Independent-loop artwork/editions | T03/T07 -> T13 -> T14: real edition, robust player, full album and authenticated remote continuation. |
| danse | Deterministic performance artwork | T04/T09 -> T13 -> T14: score/music/cut, live/spatial/installation, rights and custody. |
| ogod | Historical audiovisual album | T08 -> T14: all recordings, rhythmic/transition comparisons, selected album and device/hosted release. |
| mavsoleum-a | Historical web artwork | T08 -> T13 -> T14: repaired archive journey, exhibition/revival and accepted hosted edition. |
| etc | Restoration/artwork identity | T01/T08 -> T14: verified original baseline, restoration preview and distinct selected release. |
| backwards-up-hill | Source-led audiovisual work | T03/T04/T12 -> T14: EDL/study, complete selected edit/mix/captions/masters. |
| cycles | Source collection / selected edition | T12 -> T14: 24 originals, faithful comparison, selected sequence/presentation. |
| noonlight | Source-led artwork | T12 -> T14: intake/context separation, comparison, selected reproducible output. |
| nrcsvs | Research/reflection artwork | T12/T13 -> T14: lineage, patch/event study, implemented behavior and complete selected work. |
| nvde | Two retained artistic lineages | T12 -> T14: ten-source map, independent studies, attributed selected outputs. |
| passing-thru | Source-led audiovisual work | T12 -> T14: listening/viewing, timecoded passage, complete selected treatment. |
| wrvng-v | Text/image/audio/video work | T12 -> T14: literal revisions, reversible study, full selected treatment. |
| god-here | Postproduction artwork and instrument | T03/T10/T11/T13 -> T14: full film, nine methods, generative instrument, retained reconstruction/installation. |

## Implementation tasks

### T00: Restore the already-approved native execution path

**Owner:** Existing execution/admission owner through ACE #12.
**Consumes:** Current native session identity, approved AV scope, policy generation, exact source heads, resource budget and custody/claims.
**Produces:** One valid bounded reservation and isolated owned source lane, with retained-checkout disposition.
**Targets:** Existing #12 bootstrap and workstream producer through their owning lifecycle. This plan changes no policy, credentials, role or guard.

- [ ] Reconcile supported repository scope, environment hydration and authenticated executor role against the existing issue. Refresh the expired attempt's authority and deadline through its owner; never replay it.
- [ ] Verify host pressure with current observations, storage pool identity and branch/worktree claim before allocation.
- [ ] Admit only the selected AV packet and its declared byte/runtime budget. Keep unrelated dispatch off.
- [ ] Record exact head, producer/reservation identities, owner, attempt limit and retention plan. Publish retained prior plans through their canonical coordination home after redaction.

**Pass:** Actual producer and reservation readback, not session registration or free disk alone. **Hold:** File unchanged admission defects once in #12; continue independent planning/read-only reconciliation.

### T01: Reconcile scope and make the portfolio navigable

**Owner:** ACE coordination plus each source owner.
**Targets:** workspace-manifest.json; tools/identity_contract.py; tools/workspace_layout.py; tools/tests/test_identity_contract.py; existing generated docs/project-catalog.md and docs/software-catalog.md; source-owned ace-manifest.json and edition registers.
**Produces:** A complete crosswalk for all 15 projects, existing issues/PRs, source records, compositions and editions.

- [ ] Pin current default/WIP heads; enumerate all pages of existing open obligations for the six implementation owners and all 15 project records. Preserve task IDs and identify superseded or already-implemented repairs.
- [ ] For each requirement record owner ID, source evidence, implementation pin, dependencies, next artifact and separate acceptance/publication/custody evidence. Use existing source registers and issue graphs; do not create a second backlog service.
- [ ] Resolve missing ownership for source-only projects from their original briefs and actual artifacts before adding a binding. An absent source gets a named retrieval owner and bounded search evidence.
- [ ] Extend existing schema/renderer only for fields absent from the current contract. Generate navigation from authored records; never hand-edit generated views.
- [ ] Provide a generated “start here” path per project to the current retained instrument, last accepted example, open next task and source owner, with private locators resolved privately.

**Tests:** Existing identity/implementation/layout suites; every manifest project represented exactly once; no duplicate engine; stale/missing evidence remains visible; no private-binding additions in public catalog.
**Commands:** python3 -m unittest tools.tests.test_identity_contract tools.tests.test_implementation_contract tools.tests.test_workspace_layout -v; python3 tools/workspace_layout.py check --catalog-only. Run separately.

### T02: Close the manifest path-boundary defect

**Owner:** ACE #13. **Files:** tools/workspace_layout.py; tools/tests/test_workspace_layout.py.
- [ ] Add regression cases for LF, CR, ASCII control bytes and DEL, including a value that would emit a second ignore directive.
- [ ] Reject these values in safe_path before PurePosixPath construction. Preserve all valid current paths and existing metacharacter escaping.
- [ ] Run the focused layout suite and catalog check. Confirm generated views and source bindings remain unchanged.
**Pass:** Invalid values raise ValueError; one manifest value cannot inject another ignore line. Scope is exactly the existing issue.

### T03: Establish a dependency-closed portable working set

**Owner:** Private media/native owner; source implementations consume their own resolver contracts.
**Targets:** Existing base/recovered-room material catalogs, native README/session, runtime file tables and implementation resolver; TMB source manifest; SIMVLTANEA edition registry and intake owner. Public coordination receives only sanitized acceptance evidence.
**Proposed allocation:** Start with already-local media. Admit at most 10 GiB additional working-set growth for the first two active projects, subject to existing storage/pressure policy and measured full dependency size. This is a cap proposal, not an allocation or an override.

- [ ] Reconcile both God-here catalogs, all frame sequences and runtime tables. Count actual payload bytes rather than directory metadata; distinguish replaced historical gaps from current unresolved references.
- [ ] Include native DAT/code dependencies, required fonts, FX/journal state, relative source mappings, frame/sample clock metadata and saved score/state. Identify the four unavailable context movies, unreadable archive, listening/identity and clean-plate gaps without fabricating replacements. Reconcile the 23 historical missing-room rows against the 56 recovered-room identities. Count all 13 sequence directories and their declared 1,026 frames.
- [ ] Extend existing amp/media_resolver.py into native material_workspace/prepare.py and build.py bindings: resolve private paths relative to a declared project/media root while preserving old-path compatibility. Reject missing dependencies and unintended external access with a precise report.
- [ ] Verify TMB's 16 existing local derivatives against source manifests. Required-media skips must make portable acceptance insufficient, never passing. Its fixed-output derivative builder is a mutating operation; do not rerun it merely to inventory media. Hydrate only an identified missing dependency into fresh outputs; never replace originals with proxies.
- [ ] After coordinating active drive users, run a safe drive-unavailable trial in an isolated owned session: cold open, picture/audio playback, edit, save, close/reopen, bounded render/export and reconnection. Preserve existing human native sessions.
- [ ] Record edition-specific dependency closure, input hashes, output identity and remaining full-resolution requirements. A preview is not original-media custody.

**Tests:** Missing file, absent sequence frame, corrupt source, relocated root, missing font/code, external mount absent, interrupted save and clean reopen. Use synthetic fixtures for resolver behavior and real media for perceptual acceptance.
**Rollback:** Retain existing resolver aliases and native files; revert only new code/settings; retain new generated work with its owner.

### T04: Complete independent media custody and restoration

**Owner:** Existing private custody owner and ACE custody tooling.
**Files:** tools/custody_original_media.py; tools/tests/test_custody_original_media.py; tools/custody_danse.py; tools/tests/test_custody_danse.py; current private inventory/receipts. Existing public docs/evidence receives redacted summaries only.

- [ ] Reconcile the inventory drift (older 353-file record versus newer 354-file copy receipt), per-file identities and loose sources. Use the runner's actual private inventory schema; the public aggregate report is not a runner input.
- [ ] Extend source enumeration to explicitly declared individual files plus directories, preserving names/metadata and refusing escapes, duplicate destinations, symlink ambiguity and mutable-source races.
- [ ] Replace hardcoded source/copy/restore destinations with validated private configuration bound to physical-device identity. Reject same-device custody, missing targets and inadequate capacity before payload I/O.
- [ ] Repair deadline accounting so wall/verification budgets measure their declared phases and remain bounded. Test cancellation/checkpoint/restart without overwriting completed or partial evidence.
- [ ] Select an independent target with measured capacity for the actual remaining source set, temporary payload and verification strategy. The current recovery SSD is insufficient. The recorded payload plus the existing 20 GiB reserve requires at least approximately 292.27 GiB / 313.82 GB before metadata overhead; remeasure actual requirements and any additional restore space. Verify existing authorized remote/offsite storage and recovery access before recommending new spending; unresolved capacity stays with the existing custody owner.
- [ ] Run a small admitted representative slice through hash, copy, independent device readback and clean restoration, including one loose file and sequence-bearing material.
- [ ] Execute remaining inventory in resumable bounded batches with a persistent lease/deadline and per-file checkpoint. Revalidate source changes before final receipt.
- [ ] Reopen restored native/project material and decode/listen/view representative restored recordings; verify every required byte hash. Record independent physical/offsite scope and recovery instructions separately.
- [ ] Reconcile Danse private Git/LFS/untracked source custody and Photos originals/live-pair coverage under their existing owners.

**Pass:** Every inventoried required source has explicit copy/readback/restore evidence on an independent qualified destination, with failures/missing sources still counted. Saved matching SHA lists alone do not pass.
**Rollback:** Preserve originals, interrupted payloads and receipts. No deletion or drive retirement is part of this task.

### T05: Make TMB acceptance truthful, then qualify shared playback

**Owner:** Existing private synchronized-generation playback owner and its retained draft, resolved through the authoritative private crosswalk.
**Targets:** Current soak observer, contract tests, packaging guards, scoped verifier/gate declaration and proof-page transport in that owner. Exact native file bindings remain in its private October 23 plan and retained draft.

- [ ] Pin and reconcile the exact retained draft from its private owner evidence with the current accepted base. Preserve existing packaging no-clobber/probe-failure guards, merge-base change selection and hidden-page audio suspension; rerun implicated checks rather than reimplementing them.
- [ ] Add cases for completed+FAIL, completed+INSUFFICIENT, incomplete execution and all required predicates PASS. Require nonzero for the first three.
- [ ] Remove synthetic scheduler boundary jumps and production monkey-patching from acceptance mode. Keep explicitly labelled diagnostic interactions separate.
- [ ] Measure transport with an independent monotonic clock and declared uncertainty, accounting for actual pauses/buffering. Require intended-rate fidelity, including an upper bound; a rapidly advancing 3.925x diagnostic result cannot certify natural 1x playback. Natural births/wraps must originate in the production scheduler.
- [ ] Run short real-media trials covering at least three natural births and wraps, later-generation navigation, eviction return, distinct seeks, non-boundary pause/resume and zero audio-source-reset promotion.
- [ ] Reproduce and repair remaining resource/frame/A-V failures in production code only after the observer establishes trustworthy evidence. Preserve accepted module pins until a versioned consumer update is verified.
- [ ] Run sustained measurement only under a current specific allowance; keep Safari and Chromium evidence independent.

**Required existing limits:** workers/decoders <=12; queue <=256; bitmaps <=12; textures <=24; frame sequence step <=1; A/V offset <=50 ms. Missing actual audio or independent clocks is INSUFFICIENT.
**Pass:** Honest harness plus observed production acceptance; code pass alone may finish the harness packet but does not finish playback qualification.

### T06: Finish hole-loop's experimental edition

**Owner:** timed-text-navigation-loop.
**Files:** experimental/six-encounters/tests/review-browser.cjs; existing browser/generation/character tests; app.js, engine.js, render.js and style.css only for reproduced defects; experimental/six-encounters/docs/EVALUATION.md.

- [ ] Pin current main and run historical integrity verification; preserve provenance/original-2017, literal wording and lockfile.
- [ ] Exercise all six encounters, native keyboard traversal/focus, Reading view, 200% zoom, narrow/reoriented viewport, reduced motion and interruption recovery.
- [ ] Measure real background/foreground behavior separately from synthetic events. Timed exposure accrues only eligible visible/ready/unpaused time; preserve the scored 5,000 ms behavior and 42x9 / 378-instance phrase field.
- [ ] Capture a regression before each necessary repair; rerun only affected shards plus historical integrity. In app.js startClock/updateStatus/openReading/closeReading, use reader-facing copy and score-derived timing labels without changing the score's literal text.
- [ ] Obtain edition-specific artistic/external-reader dispositions and verify the hosted candidate at its exact revision, including physical Safari coverage where required.

**Commands:** npm --prefix experimental/six-encounters test; npm --prefix experimental/six-encounters run test:review; its test:browser under the single heavy slot.
**Pass:** A selected experimental edition with behavior, source integrity, audience access and publication evidence. Historical hosting is a separate existing release.

**Full roadmap retained:** After C1 acceptance, follow existing docs/ROADMAP.md through C2 authored edition, C3 grammar/writing, C4 sound/performance, C5 reuse/services and C6 institutional operation at their existing activation conditions. Use one-parameter-at-a-time type/spatial interval/memory/color comparisons for artistic evolution; artist selection determines promotion. Preserve dormant conditional capabilities with owners instead of treating an unactivated service as complete or a prerequisite for the static edition.

### T07: Evolve SIMVLTANEA lifecycle and deliver actual editions

**Owner:** Independent-loop compositor; existing issue 27 for remote album continuation.
**Files:** src/simvltanea/browser/browser.runtime.js; editions/registry.json; docs/authoring/TMB_COMPOSITION.md; existing edition builder/importer, runtime tests and README.

- [ ] Correct documented runtime filename references and identify the current owned checkout. Reuse existing 2-7-loop layouts, audio, rendering and accepted importer.
- [ ] Reproduce cancellation during start, audio-context interruption, page visibility, reload and repeated initialization. Add explicit Play/Pause/Resume/Replay controls, recoverable lifecycle states, remembered pause intent during start, bounded event history and disposal/object-URL cleanup in the existing runtime. Preserve existing 256 MiB asset and soundtrack bounds until measured bounded alternatives are admitted.
- [ ] Preserve independent source clocks and real audio policy across pause/recovery/orientation. A failed or unavailable asset gets an explicit retryable state; retain score/edits.
- [ ] Make one real edition with actual selected media, listened mix, deliberate layout/orientation, export and replay. Compare meaningful composition choices instead of treating engineering geometries as artistic approval.
- [ ] For simvl-live, preserve the exact named Photos album, Live Photo-only selection, copied originals and full-album configuration. Use a bounded metadata census before local-original/export checks. import_photos defaults and keep-existing do not guarantee preservation: select explicit copy mode and fresh canonical var/project/export roots, and add collision/refusal tests before admitting any resume into an existing output. Never symlink working media into Photos or empty active staging. Use build_edition --limit only for labelled bounded previews; never relabel the preview as complete album ingestion.
- [ ] Implement issue 27's authenticated paged/cache-bounded resolver in its existing source owner after proving backend feasibility, byte/range/auth behavior, expiry, offline recovery and zero new spending. Do not depend on unreliable arbitrary public links.
- [ ] Complete full selected-album coverage in bounded resumable batches, then physical iPhone/background/network/endurance acceptance and owner-hosted delivery.

**Verified preflight interfaces, to run only in an owned checkout:** python3 -m tools.editions.build_edition simvl-live --limit 12 --dry-run prints planned commands; python3 -m tools.media.catalog_photos --include-live-photos --limit 100 --dry-run performs bounded metadata inspection. Do not add --check-local to the first census, and do not treat import_photos --dry-run as a cheap metadata-only operation.

**Tests:** Extend existing test_browser_runtime.py, test_browser_audio.py, test_browser_boundaries.py, test_browser_continuity.py and test_preview_staging.py for cancelled/busy starts, interrupted audio retry, repeated lifecycle/disposal, stable relative phases, bounded logs and safe staging. Physical-device observations remain separate.

**Pass:** One accepted real edition may release independently; full-album and remote-backend obligations remain open until their own predicates pass.

### T08: Complete historical-web integration and artwork restoration

**Owner:** generative-multimedia-spatial-environment, existing navigation PR 138, offline PR 182, publication-needs.json and artwork records.
**Targets:** Existing navigation/gallery/audio/cache/publication modules and their own tests. Reconcile landed catalogue PR 143 and publishing PR 145 rather than repeating them.

- [ ] Inventory current branch/PR diffs and resolve native entrance, cold-chamber navigation, history/search, gallery input and retryable loading against current main. Reconcile existing fixes for js/page.js initialization-after-fetch-failure and removed fadeOut handling, plus cache namespace collision between sw.js and js/media/cache/MediaServiceWorker.js.
- [ ] Integrate offline behavior with explicit cache identity, bounded storage, missing-media states and recoverable retries. Preserve available capabilities when authentication is missing.
- [ ] Complete issue 144's credential and no-credential runtime obligations for all four publication exhibits named by publication-needs.json; keep absent credentials visible.
- [ ] For OGOD, verify all 29 restored recording bindings, actual audio-clock-driven visual behavior and consecutive-track transitions. Compare the restored 2D work and later 3D treatment with provenance intact.
- [ ] For mavsoleum-a, complete the existing exhibition/revival issue 139 after its foundation/navigation/discovery dependencies. Verify a complete archive journey including music/diary, keyboard lightbox/focus, discovery, navigation and exhibition. Generated catalogue records need source-grounded identity/caption review; their presence is not artistic approval.
- [ ] Resolve etc's precise project/2017 baseline association; produce an isolated restoration preview and retain the evolved instance and recovery path.
- [ ] Verify exact hosted artifact revision, real media, deep links, interruptions and selected supported devices for each released artwork. Update stale STATUS prose from current receipts.

**Pass:** Integrated runtime evidence and edition-specific selection/publication, not catalogue availability or PR merge alone.

### T09: Finish the Danse private performance and capture package

**Owner:** Existing canonical private deterministic-performance source, with custody in T04.
**Targets:** Retained source score/engine, portable runner, input hydration, audio/capture/export paths and the open changes identified by its authoritative private crosswalk.

- [ ] Reconcile locally advanced commits and open PRs before selecting exact owned integration head; preserve all retained work.
- [ ] Hydrate original required inputs through current private manifests; expose missing material without substitute success.
- [ ] Reproduce portable score failures; repair deterministic execution and source-clock/audio behavior with focused tests.
- [ ] Produce the score-driven audio/capture package, repeat the render with declared reproducibility level, and reopen it from its clean handoff.
- [ ] Complete perceptual/artistic review, use-rights disposition and selected delivery format; keep private source distinct from any public edition.
**Full scope:** Preserve the exact root and child IDs in the private owner crosswalk, including music, final cut, spatial sound, public delivery, installation, rights, custody, submission and real first-order ambisonic output obligations. Reuse pure scoreAt/eventsBetween and choreography poseAt with the same owned score clock and sound RNG identity. A finite recording does not complete the unbounded live work.

**Pass:** Repeatable, reopened, listened/viewed accepted outputs plus complete final-cut, live, public/installation and rights/custody accounting in the existing owners.

### T10: Reconcile God's Ears native workbench and qualified foundation

**Owner:** Postproduction, native draft PR 62 and existing P0-P3/F01-F06 tasks.
**Physical composition owner:** compositions/comp-001; projects/god-here remains its compatibility alias. Never fork a duplicate composition directory.
**Files:** docs/GOD-HERE-EVOLUTION-2026-10-13.md; docs/GOD-HERE-QUALIFICATION.md; existing source, execution, review, material-workspace and composition records.

- [ ] Close existing issue 117 in amp/core.py and tests/test_composition.py: reject NaN, positive/negative infinity, booleans and strings for shot boundaries, while preserving finite ordered/contained source-pass-through positives. Then reconcile native draft, current Studio deployment/source, saved review state and prior accepted treatments. Preserve saved native versions, learning guide and original source.
- [ ] Complete language/speaker/breath/cut-handle/tail qualification for the selected source and subsequently the full source. Recorded speech, script, captions and inference remain distinct.
- [ ] Compare existing dialogue/room/foley/color candidates at matched listening conditions; retain raw outputs and accepted r2 evidence with its original limits.
- [ ] Finish the retained ending passage and one contrasting probe, then a 20-30-second A/B/C/D composition proof. Preserve an uncropped proportional unobstructed full-frame reference.
- [ ] Repair actual text-scaling and operator-friction problems across UI text, captions and expressive typography. Extend web/studio/core.mjs sourceMoment mappings with validated source/output maps so changing tools retains corresponding source content through retiming, rather than merely equal elapsed seconds. Test 390x844, 844x390 and 200% text; physical device evidence is separate.
- [ ] Record native/browser differences, save/reopen/replay and source-clock coupling. Provide reversible source/processed comparison and recoverable edits through existing surfaces.

**Pass:** Qualified foundation and selected proofs, not the full film, AI program or reconstruction.

### T11: Complete the full God's Ears production program and retained scopes

**Owner:** Master issue 63 and existing older epics. Reuse the 53 exact tasks / 38 deliverable bundles; their source interfaces, paths and acceptance assertions govern each implementation packet. Their planned APIs must first be reconciled with current source: amps.study.v1 is proposed, while the inspected execution dispatcher admits four existing native adapter families. Retain legacy amp/generation.py scheduling while planned amp/composition/{containers,schedule,record,supervisor}.py and web/studies/performance-adapter.mjs add the distinct multiscale capability. Current amp/composition.py already exports resolve_composition(selection=None, *, root=None): before introducing that package, perform an explicit compatibility migration preserving this import/signature through package __init__.py (or use a nonconflicting owned namespace). Run existing resolver/CLI regressions alongside the new cascade tests; never silently shadow the existing module.

| Milestone / workstream | Existing tasks | Required retained outcome |
| --- | --- | --- |
| M0 shared foundation | 64-69 / F01-F06 | Reuse/source register, benchmark/vocabulary, typed contracts, admitted measured environment, fixed dispatch, comparison/qualification. |
| Picture-guided sound | 70-73 / W01 | Addressable palette, listened comparisons and separated-event instrument study. |
| Persistent surfaces | 74-77 / W02 | Validated shot representation, surface edits, three material transfers and qualified coverage. |
| Learned connections | 78-82 / W03 | Reviewed phases, retrieval/TCC comparison, transition graph, random/authored/learned comparisons and expansion. |
| Motion | 83-87 / W04 | Trajectories, learned magnification comparison, line/type/room transfer, reviewed studies and reusable controls. |
| Optics | 88-92 / W05 | Qualified targets, three relighting states, independent optical consequences, time-dislocation studies and coverage. |
| Acoustic spaces | 93-96 / W06 | Admitted acoustic states, speech-integrity review, coupled/independent room controls and two studies. |
| Residue/disagreement | 97-100 / W07 | Exact residuals, normalized comparison, visible model disagreement, controls and discarded-film study. |
| Semantic feedback | 101-104 / W08 | Observation/interpretation records, render-describe-retrieve cycles, two lineage comparisons and inference-free replay. |
| Experimental editor | 105-108 / W09 | Bounded candidates, honest choices/ties/rejections, three-round experiment and evidence-qualified preference benchmark. |
| Integration/delivery | 109-116 / I01-I08 | One Studio collection, The Discarded Message, all nine methods, recursive instrument, new/replay proof, full-film H/V, hosted/device and clean rebuild. |

- [ ] Preserve and crosswalk the older 37-item foundation and 38-task edition obligations, including thirty-view reconstruction and installation. Reuse can satisfy equivalent assertions only with cited evidence; no master replacement or batch closure.
- [ ] Implement the existing proposed SourceSpan, MaterialRef, StudyBinding, StudyContext, StudyResult and PerformanceRecord contracts through F03/F05. Use fixed operators; no arbitrary command/import/remote-URL execution. Private context never enters public receipts.
- [ ] Sequence M0 -> M1 sound/surfaces/connections -> M2 motion/optics/acoustics/residue -> M3 semantic/editor -> M4 integrated artworks -> M5 recursive live -> M6 device/rebuild. Respect exact task dependencies and resource admission within each milestone.
- [ ] Bind source spans to integer half-open frame/sample domains and rational timebase; record resampling. Preserve source, container-local and output clocks and dependent matte/prop coupling.
- [ ] Use offline prepared materials and persistent bounded live buffers. Reconcile proposed depth 4, audio voices 24, expressive visuals 12 plus protected reference, pending events 256 and lookahead 10 seconds with measured device byte/compute caps before heavy admission.
- [ ] Complete the program's exact comparison predicates: review copies within 0.5 LU; residual float fixture closure <=1e-6; 12 held-out reviewed joins; two three-iteration semantic chains; four candidates per round for three rounds with at most two primary variables; preference fitting only after at least 30 explicit judgments across three notes with one held out.
- [ ] Produce three structurally different new performances at three concurrent scales with composite reuse and two-way modulation. Reserve decision-graph identity in durable history; replay a realized record without new inference. History failure/domain exhaustion must not silently repeat material labelled new.
- [ ] Deliver the 45-60-second The Discarded Message H/V study, the selected full-film H/V edition with captions/stems/source-output map, the complete method collection and the multiscale live instrument.
- [ ] Complete a bounded ten-minute no-input live run, cancellation/checkpoint/reload/rotation, physical iPhone/Safari review, owner-hosted access, clean-environment replay and full deliverable accounting.
- [ ] Continue reconstruction/installation with shot/venue-specific identity, gesture, occlusion, moving-camera and operator-recovery evidence. Crops/inference are never called recovered original coverage.

**Accounting pass:** Every one of 38 program bundles plus retained older scope has an independently inspectable disposition; unmet gates retain exact owners and remain incomplete. **Production completion:** Every required bundle and retained obligation is actually fulfilled and accepted at its required technical, perceptual, artistic and delivery levels. A blocked/failed technique remains unfulfilled even if an artwork omits it; accounting completeness never substitutes for production completion.

### T12: Complete source-led development for the remaining works

**Owner:** Each project's existing project ID, original brief/source archive and subsequently verified implementation binding.

| Project | First concrete artifact | Evolution and completion boundary |
| --- | --- | --- |
| backwards-up-hill | Treatment-linked source EDL/edit study with actual footage, takes and speech. | Preserve four views / three physical sensors; listened joins and measured synchronization; selected full edit, masters and source map after scoped production. |
| cycles | Exact 24-image comparison viewer with hashes/dimensions and original access. | Reconcile intended sequence/presentation from the source brief; preserve image appearance; produce and artistically select an edition, with accessible delivery. |
| noonlight | Original-identity collage comparison and development brief. | Distinguish artwork from contextual screenshot, define composition/presentation from source evidence, then deliver selected output and provenance. |
| NRCSVS | Source-cited reflection patch and bounded event study. | Implement the supported participatory/reflective behaviors from the retained brief, prove lineage/entry/exit/residue, then selected performance and recovery. |
| NVDE | Separate corruption and painted-commission studies with ten-source mapping. | Retain attribution and independent lineages, compare compositions, qualify display/output and publish only eligible selected editions. |
| passing-thru | Timecoded listening/viewing and source-bound audiovisual passage. | Resolve source intent, develop a complete selected passage/edition, preserve exact source-result relationships and real playback. |
| wrvng-v | Literal poem/photo/video/audio comparison and reversible passage. | Retain text revisions, source clocks and original media; finish selected composition, listened/viewed exports and edition evidence. |

- [ ] Recover each named intake and its brief with bounded source search; identify missing originals and an owning retrieval task.
- [ ] Resolve the intended complete deliverable from source evidence before coding beyond the first study. Record substantive unresolved artistic choices with a concrete comparison for selection.
- [ ] Use existing functional capabilities when appropriate; add an implementation binding only with demonstrated ownership and source evidence.
- [ ] Implement/produce the first artifact, review it, then complete the retained project-specific scope in independently verifiable packets. First-study completion never closes the project.
- [ ] Pass source integrity, accessible presentation, media decode/listening, reproducibility/reopen and publication eligibility before release.
**Pass:** Every project has a source-supported deliverable definition, actual selected output and complete remaining-obligation accounting. Missing source facts remain actionable retrieval work.

### T13: Make the current build usable as a composition instrument

**Owner:** Existing source UI/CLI/native owners; no additional application or parallel renderer.
**Consumes:** Qualified material/score contracts and T03/T06/T07/T10/T11 failures or review findings.
**Produces:** A coherent everyday workflow across supported existing surfaces.

- [ ] Provide the same project/edition identity and material provenance when entering via CLI, Studio or native guide; retain existing paths/interfaces and explicit backend differences.
- [ ] Make the primary flow source -> compare -> compose -> save/replay -> export visible in existing controls. Keep technical diagnostics available without making them the creative task.
- [ ] Provide reversible bypass/A-B comparison, named score/material presets and clear saved/unsaved state. Do not silently apply a destructive selection.
- [ ] Separate creative controls for vocabulary, rate, simultaneity, temporal depth and intelligibility. Preserve source reference and explicit clock/displacement behavior.
- [ ] Make missing-source, unavailable-method, interruption and resource-pressure states actionable. Keep the saved composition recoverable and prevent unexpected playback during restore.
- [ ] Validate with actual tasks: open last study, compare two treatments, change one expressive dimension, save, replay and export; record timecoded friction and repair reproduced issues.

**Tests:** Keyboard/focus/text enlargement, native saved-state persistence, identical score identity across orientations, cancel/restore, explicit missing input and bounded resources. Human artistic preference remains distinct from usability completion.

### T14: Release, verify and close out every owner without losing scope

**Owner:** Each source/edition owner; ACE derives portfolio status.
**Targets:** Existing edition/acceptance registers, current issue graphs, owner README/handoff and public-safe coordination records.

- [ ] For every selected edition assemble exact source/code/model/recipe pins, qualification, media/output hashes, supported-device observations, editable score and clean-replay instructions.
- [ ] Record artistic selection and distribution permission for that exact edition, including credited sources and dependency terms. Keep unknowns assigned; they hold only affected output.
- [ ] Publish through the existing owner and established hosting/package route. Read back actual hosted bytes/version, deep links, audio/video and access states.
- [ ] Verify source merged ancestry, running/deployed revision and observed behavior independently. Submit one exact head through the applicable merge rail; do not wait synchronously for CI or call queued merged.
- [ ] Run clean restore/reopen/replay appropriate to the artifact. Keep original/source custody distinct from distribution copy verification.
- [ ] Reconcile all 15 project records, existing issues, 53/38 God's Ears program crosswalk and older scopes; preserve unmet obligations and human-held choices in their existing owners.
- [ ] Record each checkout retained for its owner or separately custody-verified retirement. Do not delete active work, raw media, native history or original drives to make closeout pass.

**Packet closeout:** Actual chosen releases have evidence; every remaining obligation has a durable owner and next predicate. **Portfolio completion:** All required project deliverables and retained capabilities are fulfilled at their applicable acceptance levels; conditional unactivated scope remains explicitly pending, never silently complete. A plan, complete accounting, checkpoint, push or merged PR is never the completion of an artwork.

## First execution queue

| Order | Packet | Completion output |
| --- | --- | --- |
| 1 | T00, then T01/T02 within owned lanes | Valid execution lane, reconciled scope and closed path-boundary defect. |
| 2A | T05 short harness packet | Truthful independent observer with focused regressions. |
| 2B | T06 hole-loop acceptance | Release-ready experimental candidate or precise reproduced repairs. |
| 3 | T03 using already-local God-here/TMB assets | Measured portable dependency set and drive-unavailable acceptance. |
| 4 | T07 actual SIMVLTANEA edition + lifecycle | Listened/viewed/exported next candidate, with full-album scope retained. |
| 5 | T04 representative custody slice, then bounded remainder | Independent restored sources; capacity gate resolved by its owner. |
| 6 | T08/T09 and T10/T12 in ready-packet rotation | Historical-web, Danse, native and source-study outputs. |
| 7 | T11 full program and T13 improvements at their dependencies | Complete authored, generative and reconstructed/installation obligations. |
| Every packet | T14 | Durable publication/evidence/retention and updated owner state. |

2A and 2B are at most two lanes; all heavy browser/native/copy work is serialized. T03 can advance earlier when it needs only read-only reconciliation. New performance/release dates are selected only after actual acceptance.

## Validation and plan review

Plan validation: all 15 projects appear in the coverage matrix; every critique C01-C15 maps to a task; all T00-T14 references resolve; hole-loop C1-C6, Danse's complete root scope and God's Ears' 53/38 and older 37/38 scopes remain represented; existing source owners/paths are checked or explicitly delegated to their private authoritative locator; no invented completion, TODO/TBD, new private binding or raw media appears. Review the dependency order against the first-packet scope and full God's Ears master.

Implementation validation: use each source owner's scoped gate for the exact changed tree, with behavior regressions for reproduced defects, synthetic fixtures for custody/lifecycle failure modes and separate real-media/device/artistic evidence. Do not run every repository's entire suite for a plan-only change. Preserve current lockfiles and include environment fingerprints in receipts.

Independent review completed on 2026-10-24. Its three material findings were accepted: preserve the existing amp.composition resolver during the proposed package migration; distinguish scope-accounting passes from actual production completion; and remove private commit/PR/issue references from this public derivative while keeping their private authoritative crosswalks. Coverage checks confirm 15 manifest projects, 15 work packets and 15 critique dispositions; relative documentation links resolve. No runtime tests or production acceptance are claimed by this plan review. Remaining artistic choices receive concrete future comparisons in their owner.

## Premortem and forced revision

**Sympathetic:** Existing source owners, playable derivatives, saved native studies, merged experimental artwork and explicit acceptance contracts allow useful packets without rebuilding the estate.

**Adversarial 1:** A polished first study is reported as complete scope. Mitigation: T01/T11/T12/T14 preserve all deliverable IDs and old obligations, and distinguish studies from accepted editions.

**Adversarial 2:** “Portable” or “backed up” is inferred from files existing. Mitigation: T03 tests full dependency closure with unavailable drives; T04 proves independent bytes and clean restoration.

**Adversarial 3:** New engine/UI features consume all effort while nothing releases. Mitigation: hole-loop and one SIMVLTANEA edition lead the release queue; shared repairs are bounded by observed failures and consumer acceptance.

**Orthogonal:** A newer branch already solved a planned repair, or the retained source brief defines a different final artwork. Mitigation: pin/reconcile exact existing work first, preserve original briefs and classify source evidence versus design proposals.

**Forced revisions already applied:** Replaced redundant TMB packaging/merge-base/visibility rewrites with verification; corrected God-here catalog count/size interpretation; retained full nine-method and legacy scopes; separated same-SSD copies from independent custody; preserved full Photos album scope despite bounded previews; mapped the God-here compatibility alias to compositions/comp-001.

## Rollback and retention

Use targeted revert commits for bad code changes, retain old interfaces while migrating consumers, and preserve earlier plans/receipts unchanged. Interrupted exports/copies/checkpoints remain with their owner. Restore saved score/native state through existing recovery controls; never reset a peer branch or overwrite original media. Publishing this plan changes no runtime, policy, credentials, source binding or artwork selection.

## Cross-references

- [ACE admission #12](https://github.com/4444J99/audiovisual-composition-system/issues/12)
- [ACE path-boundary #13](https://github.com/4444J99/audiovisual-composition-system/issues/13)
- [Functional identities](../../docs/naming-responsibility-contract.md)
- [Composition evidence lifecycle](../../docs/composition-evidence-lifecycle.md)
- [Custody continuation](../../docs/workstream-continuation.md)
- [Hole-loop evaluation](https://github.com/4444J99/timed-text-navigation-loop/blob/068ef112f0ec624549b065d0ce72981cc20121b7/experimental/six-encounters/docs/EVALUATION.md)
- [SIMVLTANEA remote album #27](https://github.com/4444J99/simvltanea/issues/27)
- [Historical navigation #138](https://github.com/4444J99/generative-multimedia-spatial-environment/pull/138)
- [Historical offline #182](https://github.com/4444J99/generative-multimedia-spatial-environment/pull/182)
- [Postproduction evolution directive](https://github.com/4444J99/audiovisual-media-postproduction-system/blob/664a47aca1f68d84c3dd5440363b1a48ba32243f/docs/GOD-HERE-EVOLUTION-2026-10-13.md)
- [God's Ears complete 53-task / 38-deliverable program #63](https://github.com/4444J99/audiovisual-media-postproduction-system/issues/63)

