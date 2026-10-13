# ACE software and capability catalog

Generated from public identity records. Implementation paths and interfaces remain owned by their repositories. Migration contracts are review-pending until their implementation branches are merged; this catalog does not assert deployment or media acceptance. Private implementation details remain in their private owners.

| Software system | Processing responsibility |
| --- | --- |
| `audiovisual-composition-system` | Coordinate stable identities, implementation responsibilities, typed relationships and generated workspace navigation without absorbing source histories. |
| `audiovisual-media-postproduction-system` | Source-addressed audio processing, spatial compositing, directed revisions, source-unit scheduling and hash-bound native execution. The amp package retains its existing public interfaces. |
| `independent-loop-compositor` | Compile independently clocked video-loop compositions with authored orientation layouts, stage browser previews, render audiovisual exports, and adapt authenticated shared playback generations. |
| `timed-text-navigation-loop` | Schedule configured text encounters and count visible, ready, unpaused exposure; compose this capability with separately authored browser scores. |
| `generative-multimedia-spatial-environment` | Compose browser scenes, analyze audio features, mix spatial stems and sequence image-grid frames within existing authored web environments. |

| Software owner | Module | Existing or compatibility path | Capabilities | Reuse status |
| --- | --- | --- | --- | --- |
| `audiovisual-media-postproduction-system` | `composition-resolver` | `amp/composition.py` | `cap-composition-resolution` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `dialogue-processing` | `amp/audio.py` | `cap-audio-processing` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `region-compositor` | `amp/core.py` | `cap-region-compositing` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `source-timed-renderer` | `amp/render.py` | `cap-region-compositing` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `person-mask-segmentation` | `amp/segmentation.py` | `cap-person-segmentation` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `directed-recipe-renderer` | `amp/direction.py` | `cap-directed-revision` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `directed-revision-renderer` | `amp/revision.py` | `cap-directed-revision` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `source-unit-scheduler` | `amp/generation.py` | `cap-source-unit-scheduling` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `source-unit-qualification` | `amp/qualification.py` | `cap-source-unit-scheduling` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `native-execution-dispatcher` | `amp/execution.py` | `cap-native-execution` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `audiovisual-effects-workbench` | `web/fx` | `cap-audiovisual-effects` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `room-stretch-renderer` | `amp/roomstretch.py` | `cap-room-audio-processing` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `workstation-handoff` | `amp/workstation.py` | `cap-workstation-export` | interfaces-preserved |
| `audiovisual-media-postproduction-system` | `authored-foley-study` | `amp/foley.py` | `cap-audio-processing` | retained-composition-specific-defaults |
| `audiovisual-media-postproduction-system` | `authored-soundstage-study` | `amp/soundstage.py` | `cap-audio-processing` | retained-composition-specific-defaults |
| `audiovisual-media-postproduction-system` | `room-refinement-study` | `amp/roomrefine.py` | `cap-room-audio-processing` | retained-composition-specific-defaults |
| `audiovisual-media-postproduction-system` | `room-rack-study` | `amp/roomrack.py` | `cap-room-audio-processing` | retained-composition-specific-defaults |
| `audiovisual-media-postproduction-system` | `roomtone-study` | `amp/roomtone.py` | `cap-room-audio-processing` | retained-composition-specific-defaults |
| `independent-loop-compositor` | `functional-public-api` | `src/independent_loop_compositor` | `cap-independent-loop-authoring`, `cap-independent-loop-preview`, `cap-independent-loop-rendering` | interfaces-preserved |
| `independent-loop-compositor` | `loop-authoring` | `src/simvltanea/authoring` | `cap-independent-loop-authoring` | interfaces-preserved |
| `independent-loop-compositor` | `loop-browser-preview` | `src/simvltanea/browser` | `cap-independent-loop-preview`, `cap-shared-playback-adaptation` | interfaces-preserved |
| `independent-loop-compositor` | `loop-rendering` | `src/simvltanea/rendering` | `cap-independent-loop-rendering` | interfaces-preserved |
| `independent-loop-compositor` | `loop-fixture-generation` | `src/simvltanea/generators` | `cap-synthetic-loop-fixtures` | interfaces-preserved |
| `timed-text-navigation-loop` | `timed-navigation` | `experimental/six-encounters/engine.js` | `cap-timed-navigation` | interfaces-preserved |
| `generative-multimedia-spatial-environment` | `spatial-scene-compositor` | `js/3d/core/SceneManager.js` | `cap-spatial-scene-composition` | interfaces-preserved |
| `generative-multimedia-spatial-environment` | `frequency-analyzer` | `js/3d/audio/AudioAnalyzer.js` | `cap-audio-feature-analysis` | interfaces-preserved |
| `generative-multimedia-spatial-environment` | `beat-detector` | `js/3d/audio/BeatDetector.js` | `cap-audio-feature-analysis` | interfaces-preserved |
| `generative-multimedia-spatial-environment` | `spatial-stem-player` | `js/3d/ogod/OGODAudioEngine.js` | `cap-stem-playback` | interfaces-preserved |
| `generative-multimedia-spatial-environment` | `image-grid-sequencer` | `js/ogod/OGODFrameSequencer.js` | `cap-frame-sequencing` | interfaces-preserved |
