# TMB to SIMVLTANEA composition verification

Verified on 2026-10-10 in installed Chrome 154.0.8037.98. The local edition plays
two authenticated TMB generations as independent SIMVLTANEA loops with spatial
stereo audio. No TMB or SIMVLTANEA playback implementation was replaced.

## Engine reconciliation

The current tracked authority is `time-moment-brief/shared-engine`. TMB main at
`44d815c978fc9b57526ff9b18165cd5b8d777b5c` contains the consumer's accepted release
`e5900ef98fa7a9644af1708e0e6c6cbbcde5b180`. SIMVLTANEA validates release ancestry
and six exact runtime-file hashes; the local candidate staging folder is not a
second authority. Both core and FOA candidate verifiers passed. No re-extraction
or source overwrite was necessary.

The engine audit passed 162 JavaScript assertions across spatial scoring,
adversarial inputs, orientation, FOA, adapter and panoramic-oracle suites. Two
FOA tests reported missing private-source media; no ambisonic-source or headset
acceptance is claimed. Direct Python authority and graph checks also passed.

## Composition and source preservation

- Implementation: SIMVLTANEA commit `fbd9c9d`, branch `feat/tmb-spatial-composition`,
  [pull request 30](https://github.com/4444J99/simvltanea/pull/30).
- Video: two eight-second, 192-frame atlases authenticated against historical
  TMB commit `cbce79dcbcf34ce214ba77cd2aa8d8bb9ed32fa5`.
- Audio: two stereo F6 excerpts authenticated against the manifest at `44d815c`.
  The inherited 12 dB preparation gain is recorded; no new normalization occurs.
- Each atlas stays one atomic media object containing four aligned source views.
  This does not assert four independent physical cameras or remeasure alignment.
- Video and AAC packet hashes, rational packet timestamps, packet durations and
  AAC priming match before and after stream-copy muxing. Both muxed streams retain
  their admitted start times, duration, frame count and format.
- Two native eight-second loops run at rate one, with offsets zero and one second.
  The sixteen-second engineering edition permits both to wrap.
- Both responsive layouts contain the full atlas. Per-loop gains are 0.8/0.6,
  master gain 0.7. Landscape pans are -0.48/+0.48; portrait centers both voices.
- The accepted shared evaluator drives panel poses. Stereo room audio uses
  SIMVLTANEA's existing panning path; these are not four-channel FOA recordings.
- Only a clean consumer checkout can build. Every staged engine file and its
  accepted release receipt must match; a fallback preview fails the build.
  Complete editions publish through an atomic no-clobber directory rename.

Private media and screenshots remain under the existing ignored proof lane:
`/Users/4jp/Workspace/.wt-agent7-simvltanea/var/proofs/tmb-spatial-composition-2026-10-10-v3`.
The two initial runs are retained alongside it. Source files and unrelated dirty work
were preserved. All participating checkouts are retained.

## Browser evidence

The final verifier binds the edition to the independent initial admission receipt,
whose SHA-256 is pinned in the verifier. Source identities, the engine pin,
composition, muxed media and served files must match this earlier record;
changing an edition and its own receipt together cannot admit different material.
Each HTTP response also authenticates its bytes before delivery. Seven checks
passed with zero browser errors:

1. Distinct sources decode with the intended independent phase offset.
2. Both complete rendered poses, including FOV, equal the accepted evaluator.
3. Output energy moves in opposing landscape directions and recenters in portrait,
   measured against each voice's simultaneous unpanned source energy.
4. Orientation preserves media/audio nodes and adds no reload, command or native seek.
5. Pause freezes composition time and silences audio; gesture resume advances and
   restores measured signal from both voices.
6. Native eight-second loops wrap while preserving phase and evolving poses.
7. Served bytes match the edition receipt before and after playback.

Unit playback rate is asserted in every sample. At composition time 8.523 seconds,
media positions were 0.495 and 1.497 seconds, a 1.003-second difference after
wrapping. Decoded-frame counts increased from 20/48 to 214/242. Both voices still
emitted signal. Measured landscape channel-energy shifts were +0.657/-0.711;
portrait shifts relative to the original sources were effectively zero.
These are bounded desktop
observations, not an endurance, loudspeaker, headset or perceptual listening test.

The [edition receipt](evidence/2026-10-10-tmb-spatial-composition-v3/edition-receipt.json),
[source admission](evidence/2026-10-10-tmb-spatial-composition-v3/source-admission.json)
and [browser observations](evidence/2026-10-10-tmb-spatial-composition-v3/browser-acceptance.json)
are stored in this private coordination repository. No media is committed here.

## Reproduction and automated governance

Use SIMVLTANEA's `docs/authoring/TMB_COMPOSITION.md` to build a fresh local edition.
Then run this repository's verifier with explicit Playwright and Chrome paths:

```text
node tools/verify_tmb_composition.cjs EDITION_DIRECTORY PLAYWRIGHT_MODULE CHROME_EXECUTABLE
```

The importer passed 25 focused tests; six Node tests reject alternate admissions,
missing poses, ineffective panning, silent resume and native resize seeks. Eight
workspace tests verify preservation and directory generation. Existing naming, structure, dependency
boundary, generated-layout, local-lifecycle and changed-Markdown checks passed.
SIMVLTANEA's normal discovery includes the importer tests in CI. The coordination
repository now runs its manifest, workspace and acceptance-guard checks in CI.
The broad historical media suite was not rerun locally for this importer addition;
the initial implementation's full remote CI and package checks passed.

An intentional missing-browser launch verified the retry path. Its failed attempt
was retained in a separate file; the corrected executable produced a passed
canonical receipt without deleting or overwriting the failed evidence. Existing
passed receipts are immutable.

Naming and structural governance can be enforced by these linters and validators
after rules are selected. Artwork titles remain independent of stable IDs and
paths; changing a title does not require rewriting media or engine ownership.
Rules should preserve aliases and migration compatibility when paths change.

## Remaining boundaries

This verifies the bounded TMB-to-SIMVLTANEA edition, not the complete TMB generation
scheduler, panoramic/XR rendering, hardware capacity or all ACE artworks.
Artist approval and real ambisonic/headset acceptance remain separate.

Read-only engine review also noted existing work outside this consumer path:
the TMB binding disposer leaves its animation callback running; the candidate
stager rereads accepted inputs and replaces files individually; provenance prose
still describes an earlier divergence. The edition uses the accepted tracked
module directly and does not execute that stager or TMB binding. These findings
are retained here for the existing engine owner, without changing their scope.

## Delivery checkpoint

Both repositories' topic branches were pushed and their remote commit identities
read back. The implementation is in SIMVLTANEA PR 30; this report and verifier
are in [system PR 1](https://github.com/4444J99/audiovisual-composition-system/pull/1).
The initial submissions were held; the corrected implementation has since merged.

The one-shot delivery submission for SIMVLTANEA `f49290f` was deferred because
its lifecycle label was missing. The existing `lifecycle:delivery` label was then
applied. The one-shot system submission at `1e3d0a5` was held by the existing
Limen merge policy. Read-only diagnosis established that its default Python lacks
`yaml`; consequently `scripts/verify.py --deploy-regex` cannot read the existing
gates registry and the policy conservatively treats the change as deployment
sensitive while advisory checks are pending. The owner is Limen's verification
environment. No policy override, repeat merge submission, CI wait or new schedule
was used for those heads. That documentation checkpoint changed no verified
runtime or importer bytes. The initial delivery hold did not invalidate the
composition's browser checks.

On continuation, read-only inspection found green checks and valid review gaps.
The corrected importer at `fbd9c9d` and rebuilt v3 edition address those gaps. The
existing configured `limen/cli/.venv/bin/python` successfully reads the gates
registry with its installed YAML dependency. Its single delivery submission
returned `MERGED` for SIMVLTANEA PR 30 at that exact head. No global Python or
policy changes were needed. This coordination PR carries the corrected verifier,
CI enforcement and receipts; its live GitHub state is the delivery authority.
