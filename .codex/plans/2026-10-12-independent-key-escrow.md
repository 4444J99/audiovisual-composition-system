# Independent recovery-key escrow

1. Inspect existing secret-manager vault metadata without reading secret values; select the existing personal 1Password vault.
2. Store the current age identity as a document without displaying its contents or placing it in Git. Reconcile any uncertain creation before retrying to avoid duplicates.
3. Retrieve the document into a new private staging directory, compare it with the original, and use the retrieved key to decrypt the external snapshot and manifest against recorded digests.
4. Preserve the original key and backup copies. Add recovery instructions and sanitized receipts locally, beside the backup and on the audit branch. Retain this checkout.
