# ACE directory and repository architecture

## Decision

Use **Audiovisual Composition System** for the whole solution and `audiovisual-composition-system` for its existing workspace. Retain **ACE** and `audiovisual-composition-engine` as historical discovery aliases. “Engine” means a reusable runtime responsibility, not the umbrella of artwork, archives, research, custody and delivery.

Keep a small **private coordination repository** at the workspace root. It owns this design, project membership and generated navigation. Existing ignored source repositories retain independent histories at their original paths. See [migration 2.0.0](migrations/2.0.0.md).

This applies EES's classify-before-naming, stable-identity, smallest-justified-boundary and one-authoritative-source principles to ACE. EES's relevant controls remain reviewed draft. This task establishes a specific directory contract, not EES certification or audiovisual acceptance.

## Directory view applied now

```text
audiovisual-composition-system/       private coordination Git root
├── workspace-manifest.json          schema 2.0.0, membership and binding authority
├── AGENTS.md, README.md, .gitignore
├── docs/                            catalog, architecture, evidence, sources, migrations
├── tools/                           generator, composition verifier, owned tests/
├── projects/<project>/README.md     generated artwork records
│   └── local/                       ignored relative source links
├── repositories/<owner>/README.md   generated repository records + local/source
├── components/<capability>/README.md
├── archives/<collection>/README.md
├── audiovisual-composition-system.code-workspace
├── engine/, tests/                  ignored existing unversioned sources
├── simvltanea/, time-moment-brief/, the-thing-without-a-name/
├── god-here/, reflect-recur/, Earlier god-here session archive/
└── temporary-work-preservation-2026-10-10/

../audiovisual-composition-engine -> audiovisual-composition-system
```

These are consolidated views of existing authorities. They do not duplicate the media or claim that physical source relocation has happened. Each view is generated from the manifest; the local links are ignored by Git and rebuilt for this workstation. Sources that were not located remain visible as Page-backed project records.

The physical workspace authority remains Portvs's `governance/workspace-manifest.yaml`. That manifest declares the shelf and runtime topology but had no ACE-specific bindings in this inspection. This solution manifest declares ACE membership, not estate-wide placement. A later physical move must be reconciled with that existing owner.

## All project names

The canonical project directories are:

```text
backwards-up-hill/  cycles/        danse/          etc/
god-here/          hole-loop/     mavsoleum-a/    noonlight/
nrcsvs/            nvde/          ogod/           passing-thru/
simvltanea/        time-moment-brief/             wrvng-v/
```

The [project catalog](project-catalog.md) maps every one to its Page, current source and appropriate profile. The repeated god-here catalog entry resolves to one project ID.

| Canonical project | Preserved name or relationship | Meaning |
| --- | --- | --- |
| danse | Danse Macabre; the-thing-without-a-name | Project ID and artistic title are independent of repository slug |
| god-here | God's Ears | Existing project slug retained; display title preserved |
| nrcsvs | reflect-recur; Narcissus | Vault association and search aliases; no duplicate project |
| mavsoleum-a | mausoleum-a; a-mavs-olevm; a-mavs-oleum | Project spelling, ChatGPT spelling and historical repository aliases |
| wrvng-v | wrung-u | Existing Page identity with alternate ChatGPT spelling |
| simvltanea | SIMVLTANEA; TripTicks | Current work and its historical instantiation |
| etc | etc | An artwork identity; never a miscellaneous directory |

Stable project IDs reuse the original ChatGPT project IDs. Existing native IDs, such as Danse's `project_id: danse`, remain authoritative within their owner. Numeric GitHub repository IDs identify repositories across redirects; current URLs are observations, not identities.

## Repository boundaries

| Responsibility | Existing or new owner | Decision |
| --- | --- | --- |
| System composition, membership, naming and migration | Private audiovisual-composition-system repository at workspace root | Justified shared coordination responsibility; small metadata and documentation only |
| Offline audiovisual postproduction and God’s Ears studies | 4444J99/audiovisual-media-postproduction-system | Reuse Python amp primitives and projects/god-here; keep this separate from local archival custody |
| Historical multimedia website, mavsoleum-a and OGOD sources | 4444J99/generative-multimedia-spatial-environment | Reuse existing source history; OGOD is an ogod/ collection in it |
| Simultaneous independent video-loop artwork | 4444J99/simvltanea | Keep its existing package, rendering, browser, edition and archive layout |
| Multicamera alignment and generation playback | 4444J99/time-moment-brief | Keep private source and derivatives; preserve active branch and worktrees |
| Danse artwork and delivery | Existing the-thing-without-a-name checkout | Retain source; resolve remote identity conflict before redirecting or moving it |
| hole-loop | Standalone timed-text-navigation-loop repository; preserve its native public, provenance, scripts, tests, verification and docs layout | Independent source history |
| Other Page-backed works | Project records with links to observed Pages | Do not create empty repositories without an implementation responsibility |

The old Danse origin `organvm/the-thing-without-a-name` currently resolves to **private** repository **4444J99/the-thing-without-a-name-screendance**, numeric ID **1320324017**. Its configured personal remote resolves to the distinct **public** **4444J99/the-thing-without-a-name**, numeric ID **1347780050**. The local project record still calls the old origin canonical. This is an authority conflict, not permission to publish the private tree or replace a remote.

## The engine is a set of owned capabilities

Do not flatten these into one new repository by name alone:

- **Danse's pure engine** stays in its artwork repository, with its `f(seed, t)`, provenance and impure-boundary invariants.
- **Shared playback modules** have their tracked authority at `time-moment-brief/shared-engine`. Current main includes the accepted module; SIMVLTANEA verifies its accepted release ancestry and exact runtime hashes. This does not require a standalone engine repository.
- **Spatial audio and choreography staging** occupy the preserved unversioned aggregate `engine/` folder. `components/spatial-audio` exposes the candidate location; the tracked TMB module remains authoritative.
- **Postproduction primitives** already live in the `amp` package of the postproduction repository.
- **Composition tests** retain their existing root `tests/` location. Component tests remain with their source owner.

On 2026-10-10, live core and FOA verification matched the candidate sources and tracked runtime graph at TMB `44d815c`. Its provenance prose still narrates an earlier divergence; this is stale commentary, not a reason to overwrite the accepted module. Use the tracked module and reviewed consumer pin. See the [composition verification report](tmb-spatial-integration-report.md) for the real-media integration and remaining acceptance limits.

## Internal layouts by profile

These are responsibility maps. Existing native names remain unless a separately verified migration changes them.

| Profile and projects | Appropriate structure |
| --- | --- |
| System composition | manifest, docs, generated project/source directories, tools, workspace configuration |
| Packaged artwork: simvltanea | Retain src/simvltanea, tools, tests, editions, examples, fixtures, evidence, docs, archive, ignored var; follow its existing governance |
| Browser artwork: danse | Retain engine, arrival.js, interaction, render, sound, pipeline, assets, rights, submission, release and native document names |
| Media playback: time-moment-brief | Retain source manifests, calibration/prototype modules, accepted shared-engine module, tools/scripts, tests and evidence; private media and custody remain separately handled |
| Postproduction artwork: god-here | Existing amp primitives; projects/god-here for scores, intervals, masks and authored styles; web for browser edition; tests and tools stay with that repo |
| Historical web collection: mavsoleum-a, ogod | Preserve original path graph, collection subpaths, dependencies and source filenames; describe lineage with manifests instead of rewriting historical sources |
| Source collection: cycles | Project/source manifest and original references; annotations and editions only when produced; preserve original image names |
| Research artwork: nrcsvs | Existing chat-vault, exports and scripts with provenance; add research/decision records only as authored, without pretending this archive is its implementation |
| Page-backed artwork records: backwards-up-hill, etc, noonlight, nvde, passing-thru, wrvng-v | Current project record and source links; future sources, research, scores, editions, implementation and evidence collections only when their material and owners exist |

Future project editions refer to a pinned engine/component and a source manifest. They do not copy an independently editable engine into each artwork. A source manifest records original identity/digest, rights, custody reference and derivative lineage; raw media does not enter this coordination repository.

## Naming contract

Project-controlled directory names use lowercase ASCII words with single ordinary hyphens. Their membership determines their meaning: `projects` collects artwork identities, `repositories` collects implementation owners, `components` collects capabilities, and `archives` collects preserved historical material.

Living authored documents use `subject-document-type.ext`, such as `directory-architecture.md` and `workspace-migration-report.md`. Chronological evidence records carry their actual event date. Lifecycle, ownership and verification state belong in metadata, not names such as final, latest, temp or new.

Native names such as README.md, AGENTS.md, pyproject.toml, Python underscores, existing package names, hashes, media source names and original archival titles are deliberate exceptions. This is not a blanket rename of imported material.

Aliases are discovery and compatibility surfaces. They may not reclassify unrelated things as one work, silently collapse distinct repositories, or weaken handling restrictions.

## Evidence and adoption

EES source chapters: [Naming metadata and compatibility](https://chatgpt.com/space/page_380217fae8608191b9284eb4c3c2dbda), [Workspace and repository architecture](https://chatgpt.com/space/page_506015c187148191bb44fa21814a8c54), and [EES report](https://chatgpt.com/space/page_6aca92c2aacc81918a0c7d48a4227298).

Local EES toolkit inspection: revision `1dab672892563537daf6c3a1ed1e66f90d06a60e`, branch `v0.2.0-semantic-review`. Relevant reviewed-draft controls are GES-ID-003, GES-ID-004, GES-ARC-001 and GES-ARC-002. The accompanying brainstorm ES-BS-008 explicitly rejects imposing SIMVLTANEA's layout universally. See [source register](source-register.md).

Directory validation proves membership, syntax, references and local navigation. It does not prove rendered-media fidelity, synchronization, audio quality, WebXR support, engine acceptance, archive completeness or remote custody.
