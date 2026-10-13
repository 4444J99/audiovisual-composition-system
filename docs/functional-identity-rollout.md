# Functional identity rollout, 2026-10-13

The migration is implemented in existing owners and submitted as connected PRs.
The postproduction companion, PR 59, merged on October 13 at `664a47a`.
Coordination is reviewed in PR 9; each other implementation retains its own
review and adoption record. These software changes do not assert media/artistic
acceptance.

| Public implementation | Review | Applied responsibility boundary |
| --- | --- | --- |
| Audiovisual postproduction | [PR 59](https://github.com/4444J99/audiovisual-media-postproduction-system/pull/59) | Neutral composition directory; source descriptions; generic compositor and selector; legacy path/API compatibility |
| Independent Loop Compositor | [PR 32](https://github.com/4444J99/simvltanea/pull/32) | Functional Python/CLI facades over the same implementation; composition/artwork/edition identities retained |
| Timed-text navigation | [PR 61](https://github.com/4444J99/timed-text-navigation-loop/pull/61) | Functional scheduler API; exact legacy alias; stacked on the existing experimental PR 59 |
| Historical multimedia presentation | [PR 164](https://github.com/4444J99/generative-multimedia-spatial-environment/pull/164) | Typed processing responsibilities with unchanged historical runtime, media and path graph |

The two existing private owners have their own draft changes and validation
records. Their new private implementation details and review links are not
copied into this public rollout document.

The postproduction change includes both the already-merged October 13 evolution
PR 57 and the subsequent rendering correction PR 58. The integration preserved
the correction's rendering/generation files exactly.

## Verified here

- All six implementation descriptors pass the same typed contract validator with
  actual repository-local paths checked. Each owner preserves its numeric
  GitHub ID and native identities.
- Coordination: 54 Python tests (49 passed; five macOS custody tests skipped in
  Linux), 14 Node acceptance-guard tests passed, and 54 generated records check
  cleanly. All 15 original project identities remain.
- The typed registry has seven systems (including ACE), 20 capabilities,
  29 public modules, three existing public sources, six compositions, 13 artwork
  records, one existing edition and four preservation archives. The source
  collection and playback-software projects are not fabricated as artworks.
- Postproduction: 357 Python tests and 249 Node tests passed after integrating
  main; includes installed-package tests and an unrelated two-region composition
  rendered with FFmpeg. Fifty-nine moved composition records retain byte hashes.
- Loop compositor: 77 focused tests and installed-wheel preview/render checks
  passed. Six full-suite setup errors reproduce unchanged on the base commit:
  missing Playwright and unavailable accepted ancestry in the neighboring
  source-only snapshot. No assertion failure was observed.
- Timed-text navigation: seven new boundary/API tests and 21 existing pure tests
  passed. Historical implementation: five descriptor tests passed.
- Accepted shared-playback runtime hashes remain unchanged. Private engine
  facade tests preserve object identity and deterministic source isolation.

An independent reviewer reproduced two publication-filter defects. Regression
tests now reject unknown/nested metadata and public source provenance pointing
to private or unknown owners. The public exporter uses explicit field lists.

## Adoption and limits

Review and merge implementation changes before relying on their new functional
entrypoints. The timed-text change stays stacked on its existing experimental
branch. The coordination catalog marks these migrations review-pending; it does
not claim its proposed paths already exist on every default branch.

CI observations are attached to each PR and may change. Local synthetic and
contract checks do not replace browser, listening, source-media, hardware, custody
or release acceptance. Chromium was unavailable for local timed-text browser
testing; the full private portable/GPU batch was not reproduced in the selective
snapshot. See each PR for its precise validation boundary.

The coordination repository remains public. Current generated redaction and
new-binding guards do not retract its previously published history. No original
media moved and no repository history was rewritten.

## Reproduce descriptor checks

From this coordination checkout, pass each authorized implementation's actual
checkout path. The command imports no runtime and prints only aggregate counts:

```sh
python3 tools/validate_implementation.py /path/to/implementation/ace-manifest.json
```

Keep private descriptors in their private owners. `--metadata-only` checks types
and relationships without claiming files exist; it is not the physical path
verification used above.
