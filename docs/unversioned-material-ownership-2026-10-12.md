# Preserved material ownership audit — 2026-10-12

This is a read-only source audit and an ownership recommendation, not a migration or backup receipt. No candidate code, media or transcript contents were staged. The file-level ledger is [unversioned-ownership-2026-10-12.json](evidence/unversioned-ownership-2026-10-12.json).

## Baseline and scope

TMB's live remote main is `44d815c978fc9b57526ff9b18165cd5b8d777b5c`, matching the cached origin/main used for comparison. The nested working checkout is on `agent5-loop-continuity` and has no shared-engine directory; it was not switched or modified. Compare committed blobs, not that checkout's working files. Danse comparison uses local HEAD `f6f27c10a4bf617d895b0f0387eb3013aa39913b`; its publication and remote-authority conflict are outside this audit. The recovery HEAD is recorded in the ledger.

Inventoried 78 regular files / 1,437,455 bytes across engine/, tests/ and four loose documents: 58 source/document files and 20 Finder/Python cache files. Exact blob matching covers the full committed trees of TMB main, local Danse HEAD and the local recovery repository. Uniqueness below is bounded to these trees and TMB's explicit extraction map; it is not a search of every branch, archive or external backup.

## Findings

All 14 candidates named in shared-engine/PROVENANCE.json match their recorded source SHA-256. Five runtime modules, seven unit-test/harness files and the audiovisual demo are equivalent after removing the known provenance preamble and rewriting relative imports. The remaining audiovisual test differs only in demo location and import-path assertions, which upstream adapted to the extracted layout. There is no newly unique runtime implementation to transplant from these five modules. The tracked shared engine remains authoritative; do not rerun an import over it.

Seventeen of the 58 source/document files have exact committed counterparts. Three prototypes, two calibration tests, six calibration tools and two Python integration files match TMB (and the recovery snapshot). Danse holds exact copies of the interaction adapter, video texture, panoramic module and unit harness. Some of those also participate in the shared-engine map; these counts overlap.

All 16 engine/tools Python scripts and all three prototypes have TMB calibration counterparts. Ten tools and test_calibration.py differ from upstream, mainly because the loose copies use COMPOSITION_ROOT or the old flattened layout. embed_real_media.py has a material difference: the loose version embeds base64 media, while current TMB uses private hydrated relative asset references. Preserve the old file as history; do not replace the current upstream privacy behavior with it.

All nine tests/engine Python files have TMB tests/e2e counterparts. Two are exact; seven differ. TMB's conftest has newer HTTP origins, derivative admission and additional tiers. The loose copies retain aggregate-root assumptions. Treat them as historical variants rather than seven new suites.

Thirteen source/document files have neither an exact blob match nor a mapped counterpart in this comparison:

- engine/examples/spatial-choreography.html
- engine/tests/unit/spatial-score-challenger.test.mjs
- engine/tests/unit/spatial-score-stress-m6.test.mjs
- tests/e2e/harness.mjs, runner.mjs, and tier1-features, tier2-boundaries, tier3-combinations and tier4-scenarios test files
- HANDOFF_AMBISONIC_INTEGRATION.md, PROJECT.md, TEST_INFRA.md and TEST_READY.md

The two stress suites target shared spatial-score evaluators and contain allocation/heap benchmarks. Their existence does not establish that those assertions pass on the authoritative module; admission requires reviewing and running them against it. The six JavaScript E2E files target the Danse checkout through DANSE_ROOT, not TMB's shared-engine package. The four documents describe the older aggregate arrangement. The handoff's unqualified “merged to main” claim is not established by this audit; retain it as a dated historical claim.

## Owner and destination decisions

| Material | Intended owner and destination | Treatment |
| --- | --- | --- |
| Five extracted runtime modules, mapped shared unit tests and audiovisual demo | Private TMB shared-engine/ | Existing committed authority; retain loose originals as historical candidates, no reimport. |
| Two spatial-score stress suites and spatial-choreography demo | TMB shared-engine/tests and shared-engine/examples on a future topic branch | Review import paths and semantics against main, then admit only useful unique coverage/demo behavior. |
| Calibration prototypes, tools and calibration tests | TMB synchronized-generation-calibration/ | Existing implementation owns this concern. Preserve older variants; port only reviewed useful deltas, retaining private-media reference behavior. |
| tests/engine Python integration suite | TMB tests/e2e/ | Existing, newer implementation owns this concern; reconcile useful deltas rather than copy the loose suite wholesale. |
| Interaction adapter and six tests/e2e JavaScript files | Danse interaction/ and scripts/tests/ | Adapter is already tracked. Preserve unique E2E candidates privately until Danse remote identity is reconciled; no push to either remote from this audit. |
| Four loose root docs | Private historical engine-candidate snapshot, with links to TMB and Danse owners | Preserve original names and text with this audit's qualification. Do not publish historical completion claims as current acceptance. |
| reflect-recur/ | Private NRCSVS conversation-vault/archive custody | Keep exports, chat-vault and acquisition scripts together; no assumption that this is the current artwork implementation. |
| Earlier god-here session archive/ | Private God's Ears session-archive custody | Preserve alongside the existing God’s Ears archive relationship, with independent history/backup; no automatic import into a public implementation repo. |
| Finder metadata and Python bytecode | Historical snapshot only if preserving an exact tree | No active source-code owner needed; no deletion performed. |

No standalone active engine repository is warranted: the functional owners already exist. The historical mixed candidates and documents need a private, immutable backup snapshot before any future cleanup; they should not become a competing runtime authority. TMB can own the engine-specific archive metadata, while Danse and the two conversation archives retain their distinct ownership. Choose a verified private backup destination rather than publishing private material into a public source repository.

## Custody and next operations

The local recovery repository proves that some copies have Git history, contradicting the blanket claim that nothing is versioned anywhere. It does not prove independent off-disk custody, and it does not contain exact matches for the thirteen bounded unique files above. Do not retire originals based on this audit.

reflect-recur contains 45 regular files / 3,326,393 bytes; Earlier god-here session archive contains 13 / 317,552 bytes. Neither has a top-level .git directory. These are size/inventory observations, not content verification or backup proof.

Next preservation operation: create a deadline-bounded private snapshot under the approved custody staging root, include originals and a SHA-256 manifest, transfer to an independent private destination, read back and verify restoration. Keep originals in place until that receipt exists. This audit authorizes no source moves, deletion, source remote changes or shared-engine staging. Subsequent code admission belongs on each source owner's topic branch after checking its local instructions and concurrent writers.
