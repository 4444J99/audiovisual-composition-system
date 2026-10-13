# Functional identities and composition boundaries

Adopted implementation brief, 2026-10-13. This contract implements the owner's
instruction to name reusable software by its processing responsibility, preserve
artistic titles as artwork metadata, and describe source footage literally.

## Identity model

| Entity | What it identifies | Identity and naming rule |
| --- | --- | --- |
| Software system | An owned, reusable processing implementation | Functional name; repository identity remains the numeric GitHub ID |
| Capability | A processing responsibility independent of its packaging | Functional ID; implemented by a module, never a duplicate engine |
| Module | An actual implementation boundary within an existing repository | Functional name plus native path and preserved interfaces |
| Source media | One registered source recording or asset | Stable source ID, literal description, original filename and provenance; artwork titles are not source descriptions |
| Composition | An authored selection, arrangement, score or generative rule set | Stable composition ID, source/module references and optional artwork relationship |
| Artwork | The artistic identity of a work | Existing project ID, title and discovery aliases; publication is a separate state |
| Edition | A particular realization or delivery of a composition | Edition ID, composition reference and exact implementation/source pins where recorded |
| Archive | Preserved historical material under its custody owner | Stable archive ID, original location and names; no relocation implied |

`workspace-manifest.json` remains ACE's sole authored membership authority. Its
typed identity registry describes the relationships above. Existing project IDs,
repository IDs, native IDs and historical aliases remain stable. Not every
project is an artwork: a playback software project is still software. An empty
source-media or edition registry means none have been verified into that registry;
it is not evidence that no sources or editions exist.

Each implementation owns `ace-manifest.json`, a small, source-controlled local
contract: `schema_version`, `system_id`, `repository`, `software`, `capabilities`,
`modules`, `source_media`, `compositions`, `artworks`, `editions`, and `archives`.
The coordination registry references an implementation by its repository ID; it
does not ingest that repository's private source registrations. Local manifests
can name retained native implementation paths as compatibility locations.

## Responsibility owners

| Functional responsibility | Existing implementation boundary |
| --- | --- |
| Audiovisual postproduction | `amp`: audio processing, segmentation, rendering, direction, source-unit scheduling and execution |
| Independent-loop composition | Existing Python loop compositor and its rendering/browser adapters |
| Multicamera playback | Existing alignment/playback implementation and accepted shared-engine module |
| Deterministic browser performance | Existing pure engine and its separate interaction, rendering and sound boundaries |
| Timed-text navigation | Existing browser text runtime and separately maintained experimental composition |
| Historical multimedia presentation | Existing historical website and collection path graph |

Existing repositories retain ownership. New functional entrypoints delegate to
the existing implementation. Package, CLI and import aliases preserve callers;
accepted playback pins and runtime bytes remain unchanged. Historical material
does not acquire a new engine simply because it has a new descriptive record.

## Access and publication

Authenticated GitHub metadata on 2026-10-13 reports coordination repository ID
`1413700288` as **public**, with the authenticated owner able to administer and
push. Earlier prose calling it private was incorrect. No visibility setting is
changed by this migration, and documentation is not an access control.

Generated public navigation omits private implementation relationships, source
locations, and private Page/local metadata. The validator freezes previously
published sensitive legacy bindings and rejects additions or changes without a
new reviewed contract. This limits new disclosure; it does not remove already
published metadata from Git history or historical evidence documents. A future
private source registry must stay within an actual private owner.

`tools/verify_repository_access.py --github` reads authenticated metadata by
stable repository ID and fails if visibility, identity or archive state differs
from the reviewed access record. CI executes the same check. Offline unit tests
use synthetic metadata; the successful authenticated observation is recorded
separately from those tests.

## Migration and acceptance

This is an additive, reversible contract migration. Functional software directory
views become canonical while old views remain compatibility navigation. Physical
source checkouts, archives and recordings stay in place. A composition may move
within its implementation owner only with old-path compatibility and tests that
preserve relative references, source digests and qualification behavior.

Acceptance requires: all 15 existing project identities survive; references are
typed and resolvable; functional modules can be addressed without an artwork
title; old supported interfaces still work; generated views reproduce exactly;
private relationships cannot leak through generated output; pinned engines and
source provenance remain unchanged. These checks do not prove media rendering,
listening qualification, device acceptance, publication or artistic completion.

The October 13 evolution implementation in postproduction PR #57 was found
already merged. Subsequent normalization starts from that merged implementation
and retains its source-review admission gate.
