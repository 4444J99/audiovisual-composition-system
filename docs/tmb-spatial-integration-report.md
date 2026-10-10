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

- Implementation: SIMVLTANEA commit `f49290f`, branch `feat/tmb-spatial-composition`,
  [pull request 30](https://github.com/4444J99/simvltanea/pull/30).
- Video: two eight-second, 192-frame atlases authenticated against historical
  TMB commit `cbce79dcbcf34ce214ba77cd2aa8d8bb9ed32fa5`.
- Audio: two stereo F6 excerpts authenticated against the manifest at `44d815c`.
  The inherited 12 dB preparation gain is recorded; no new normalization occurs.
- Each atlas stays one atomic media object containing four aligned source views.
  This does not assert four independent physical cameras or remeasure alignment.
- Video and AAC packet hashes match before and after stream-copy muxing.
- Two native eight-second loops run at rate one, with offsets zero and one second.
  The sixteen-second engineering edition permits both to wrap.
- Both responsive layouts contain the full atlas. Per-loop gains are 0.8/0.6,
  master gain 0.7. Landscape pans are -0.48/+0.48; portrait centers both voices.
- The accepted shared evaluator drives panel poses. Stereo room audio uses
  SIMVLTANEA's existing panning path; these are not four-channel FOA recordings.

Private media and screenshots remain under the existing ignored proof lane:
`/Users/4jp/Workspace/.wt-agent7-simvltanea/var/proofs/tmb-spatial-composition-2026-10-10-v2`.
The initial run is retained alongside it. Source files and unrelated dirty work
were preserved. All participating checkouts are retained.

## Browser evidence

The final verifier authenticated every served preview file before and after
playback, including media, plan, runtime, adapter and shared module. Seven checks
passed with zero browser errors:

1. Distinct sources decode with the intended independent phase offset.
2. Rendered poses equal direct evaluation by the accepted shared module.
3. Both real audio sources emit nonzero stereo signals with layout-derived pans.
4. Orientation preserves media/audio nodes and adds no reload or seek events.
5. Pause freezes composition time and silences audio; gesture resume advances.
6. Native eight-second loops wrap while preserving phase and evolving poses.
7. Served bytes match the edition receipt before and after playback.

At composition time 8.523 seconds, media positions were 0.496 and 1.493 seconds,
a 0.997-second difference after wrapping. Decoded-frame counts increased from
21/49 to 214/242. Both voices still emitted signal. These are bounded desktop
observations, not an endurance, loudspeaker, headset or perceptual listening test.

The [edition receipt](../evidence/2026-10-10-tmb-spatial-composition/edition-receipt.json),
[source admission](../evidence/2026-10-10-tmb-spatial-composition/source-admission.json)
and [browser observations](../evidence/2026-10-10-tmb-spatial-composition/browser-acceptance.json)
are stored in this private coordination repository. No media is committed here.

## Reproduction and automated governance

Use SIMVLTANEA's `docs/authoring/TMB_COMPOSITION.md` to build a fresh local edition.
Then run this repository's verifier with explicit Playwright and Chrome paths:

```text
node tools/verify_tmb_composition.cjs EDITION_DIRECTORY PLAYWRIGHT_MODULE CHROME_EXECUTABLE
```

The importer passed 17 focused tests. Existing naming, structure, dependency
boundary, generated-layout, local-lifecycle and changed-Markdown checks passed.
SIMVLTANEA's normal discovery includes the new tests in CI. The broad historical
media suite was not rerun for this importer-only addition.

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
Neither submission is recorded as merged.

The one-shot delivery submission for SIMVLTANEA `f49290f` was deferred because
its lifecycle label was missing. The existing `lifecycle:delivery` label was then
applied. The one-shot system submission at `1e3d0a5` was held by the existing
Limen merge policy. Read-only diagnosis established that its default Python lacks
`yaml`; consequently `scripts/verify.py --deploy-regex` cannot read the existing
gates registry and the policy conservatively treats the change as deployment
sensitive while advisory checks are pending. The owner is Limen's verification
environment. No policy override, repeat merge submission, CI wait or new schedule
was used. The subsequent documentation checkpoint changes no verified runtime
or importer bytes. This is a delivery hold, not a failure of the composition's
passing browser checks.
