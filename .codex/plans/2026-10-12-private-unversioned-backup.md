# Private unversioned backup

1. Verify mounted destination identity and free space; use the existing independent T7Recovery custody destination. Preserve originals.
2. Inventory the eight declared roots, including hidden files and empty directories, under a bounded deadline.
3. Create a metadata-preserving archive in private staging outside vendor runtime state. Encrypt before copying to the unencrypted external volume; retain the key separately on FileVault-protected storage.
4. Read back from the device, decrypt and restore into a new private tree; verify bytes, paths and metadata. Preserve original macOS security attributes in an encrypted sidecar and record extraction differences explicitly.
5. Publish only sanitized verification evidence. Retain originals, staging, restore, key and interrupted receipts. No retirement or deletion.
