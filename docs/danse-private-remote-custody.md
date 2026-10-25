# Danse private remote custody preparation

**Custody is not complete.** Two remote destinations are prepared, but no source
archive has been uploaded, no complete remote copy has been read back, and no
clean restore has been verified. Originals and partials remain retained.

The dedicated [private GitHub repository](https://github.com/4444J99/danse-private-custody)
is numeric repository ID **1416283322**, verified private, active and writable.
Its initialization commit contains only an explicit incomplete-status README;
the README blob was read back and matched. This commit does not preserve Danse's
local-only objects, stash or ignored files.

A separate Google Drive folder, **Danse Private Custody 2026-10-12**, was created
in the connected user's My Drive. Its metadata returned `shared: false` and one
user permission with role `owner`. Its exact folder ID is held in the private
destination receipt; the redacted evidence publishes only its SHA-256. GitHub
and Google Drive are the proposed independent provider destinations. This is
provider separation, not a claim of verified archive copies or independent
account-recovery testing. Google Drive authentication and ample available account
capacity were also observed through rclone; connector/rclone account binding
must be reconciled privately before any rclone upload to the new folder.

An earlier rclone mkdir/readback for a differently named folder timed out.
Its outcome remains unknown and no deletion or overwrite was attempted. The
connector-created folder has a distinct, verified identity, so it need not be
confused with that unknown partial operation.

The [redacted preflight receipt](evidence/danse-private-remote-preflight-2026-10-12.json)
records the actual current blockers: host admission denied heavy work at
**85.59% swap**, `vitals-shed` and an unavailable pressure sensor. Local free
space was about 16.8 GiB, below the existing runner's 20 GiB reserve. Neither
T7Recovery nor Archive4T is attached. No heavy acquire or payload I/O was started
under this denial. Moving the destination to a private repository does not
remove the archive/readback/restore workload's admission requirements.

The [remote custody plan](../.codex/plans/2026-10-12-danse-private-remote-custody.md)
defines the remaining work: preserve the entire Git store and material with
native metadata, verify actual transport/storage limits, upload both copies,
read them back independently, and restore and check every original entry plus
Git refs, stash reflogs and fsck. The existing disk-oriented runner does not
implement that remote transport. The new remote path is prepared for review,
not presented as an implemented or successfully exercised archive runner.

Draft PR #5 remains the review home for redacted evidence. PRs #2 and #3 were
already merged outside these custody attempts. No source history, source remote,
original filename, active peer workload or admission policy was changed here.
