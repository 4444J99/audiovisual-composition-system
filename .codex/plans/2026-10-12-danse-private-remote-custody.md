# Danse private remote custody

User authorized completion using the private-repository alternative. Preserve
originals; obtain two independent copies and a clean restore; keep draft PR #5.

1. Verify private destination ownership/access and provider independence.
2. Capture the complete standalone Git store, including local refs, objects and
   stash reflogs, plus all working-tree material and native metadata. Do not
   rewrite source histories, remotes, paths or filenames.
3. Under successful fresh host admission and capacity checks, produce an archive
   with a complete private checksum/metadata inventory and source-drift checks.
4. Publish one complete archive to the dedicated private GitHub repository and
   a second to the verified private Google Drive folder. Check actual GitHub
   archive transport/LFS capacity before uploading; a control commit is not a
   source copy. Do not reuse either source repository as coordination history.
5. Independently download both copies and compare archive digests. Restore into
   a fresh private directory; compare all material hashes/metadata, Git state,
   both stash reflog entries and tracked status; run Git fsck. Retain all originals
   and partials. Publish only redacted evidence in the coordination review.

Prepared: private GitHub repository 1416283322 and a new, unshared Google Drive
folder with owner-only returned permission metadata. The GitHub control README
was committed and read back. No source archive was uploaded. An earlier rclone
folder creation/readback timed out with unknown outcome; retain that observation
and use the separately identified connector-created folder for this plan.

Blocked: fresh host status at 00:50:34 UTC on 2026-10-13 (20:50:34 EDT on Oct 12)
denied heavy work at 85.59% swap, vitals shed and an unavailable Backblaze sensor.
Local free space was 18,044,506,112 bytes, below the existing disk runner's 20 GiB
reserve even before archive/restore staging. Neither physical custody disk is
attached. Remote storage resolves destination availability, not host admission.
No payload archive, independent readbacks or clean restore have completed.

Resume predicate: host pressure sensors available and real heavy acquisition
allowed; a reviewed remote transport with sufficient staging/restore capacity
and fresh source stability. Do not override pressure gates or silently lower
the current reserve to manufacture completion.
