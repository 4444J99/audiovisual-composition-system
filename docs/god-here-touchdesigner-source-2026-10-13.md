# God-here native TouchDesigner source stage — 2026-10-13

God-here / God's Ears is the composition target. Its active software and
`compositions/comp-001` definition belong to
[audiovisual-media-postproduction-system](https://github.com/4444J99/audiovisual-media-postproduction-system/tree/664a47aca1f68d84c3dd5440363b1a48ba32243f/compositions/comp-001).
The preserved God-here archive remains source material. This coordination record
documents a native session stage; it does not transfer implementation ownership.

## Verified live source stage

The existing `audiovisual-sampler-01.toe` session, running TouchDesigner
2025.33230 with Python 3.11.15, initially had an empty `/project1`. A contained
`/project1/base_godhere` now provides source picture, paired movie audio and
native playback controls. The project file was neither reloaded nor saved.

The original source filename was preserved. Its SHA-256 matches the registered
`comp-001` source:
`bde1c7e0910941f8ca3bce06e8c2ddb3a31da4335b544fd041d84e97d1060225`.
TouchDesigner opened and decoded it as 1280 × 720, 30 fps, 3,360 frames and
112 seconds, with two audio channels at 44.1 kHz. No required media is missing
from this source stage. Private media locations and component snapshots remain
outside Git.

All paths below are relative to `/project1/base_godhere`:

| Signal | Native route |
| --- | --- |
| Picture | `movie_source` → `null_picture` → `out_picture` |
| Audio | `audiomovie_source` → `math_gain` → `null_audio` |
| Monitor | `null_audio` → `audio_output` |
| Composition audio endpoint | `null_audio` → `out_audio` |

`audiomovie_source` references `movie_source`, so picture and audio share the
movie clock. The full decoded frame passes through without cropping or
treatment. Audio remains the source's stereo camera mixture. The monitor uses
the system default output device, a gain of 0.25, the native 150 ms output
buffer and the native -150 ms audio sync offset. Physical audibility and
perceptual synchronization have not been accepted.

The component's **God-here** parameter page exposes `Sourcefile`, `Play`,
`Speed`, `Cuepoint` in source seconds, the `Cue` pulse, `Volume` and `Mute`.
`Play` is initially off, `Speed` is 1 and `Cuepoint` is 85.1333333333 seconds.
Pulse **Cue on the parent component**. The global TouchDesigner timeline must
also be playing for continuous playback.

## Runtime verification

A bounded 1.5-second live probe advanced the uploaded source frame from 2554
to 2599, exactly 45 source frames. The source audio measured a peak of
0.4035738 and RMS of 0.1326135; after the 0.25 gain, the audio endpoint measured
a peak of 0.1008935 and RMS of 0.0331534. These measurements establish decoded
audio flowing through the route, not a listening judgment.

The probe automatically stopped the source and restored the original paused
global timeline at frame 302. A later inspection observed the timeline paused
at frame 126; it was not forced back. The source was recued to frame 2554.
Both output endpoints were explicitly cooked and inspected. The component's
error check returned zero errors; the signal graph had no cycles. Annotation
containment and separation checks passed.

The installed integrations are official TDMCP 1.1.55 and td-atlas 0.3.0. Their
live CLI tool calls work against this session. Schema lookup uses td-atlas's
runtime-probed 2025.33230 index rather than assuming an older parameter catalog
matches this build.

## Remaining composition work

This stage is the verified source basis for the native composition. It does
not implement the five performer treatments, source-synchronous masks,
micro/meso/macro containers, edition routing or generative instrument.

The pinned `comp-001` definition retains P01 pressure, P02 lag, P03 refraction,
P04 residue and P05 erosion, its two camera layouts, six shots and twenty
authored cue intervals. Those assignments remain authored trials with artist
acceptance pending. The October 13 evolution plan additionally requires an
unobscured reference anchor and independently addressable performer fields.
Speaker identities, word timings and isolated voices must not be inferred from
the source mixture or provisional transcript.

Future native changes should preserve the source endpoint and paired audio,
use source time for performer fields and masks, and remain contained so the
artist's manual network changes survive. No render, media upload or dependency
installation is needed for the next composition step.
