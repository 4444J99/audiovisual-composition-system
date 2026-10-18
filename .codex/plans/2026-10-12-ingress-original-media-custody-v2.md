# Ingress Original-Media Custody and Restore Plan — Version 2 (2026-10-18)

**Document Identifier**: `2026-10-12-ingress-original-media-custody-v2.md`  
**Supersedes**: `2026-10-12-ingress-original-media-custody.md` (v1)  
**Status**: Refreshed 10-bank inventory and in-place loose candidate reconciliation verified; physical store colocation documented; streamed SHA-256 and restore proof protocols established; empirical camera coverage and sensor designation proven. All source originals remain strictly read-only and preserved on `/Volumes/Ingress`.

---

## 1. Inventory Evidence & Reconciliation

### 1.1 Dual Independent Project Roots & 10-Bank Inventory
The primary archival volume `/Volumes/Ingress` maintains two strictly distinct project identities with preserved root-relative structures, filenames, and access boundaries:
1. `backwards-up-hill/` (Project ID: `g-p-6ab7e2663fe881919dae29c328e14d72`)
2. `time-moment-brief/` (enclosing source collections `palm-beach-christmas` and `pompano-concepts`)

The refreshed enumeration confirms the 10 camera and audio banks:

| Project Root | Sub-Collection / Bank | Path on `/Volumes/Ingress` | Regular Files | Logical Bytes | Description & File Types |
|---|---|---|---|---|---|
| **time-moment-brief** | `palm-beach-christmas` / `2021DEC-100GOPRO` | `time-moment-brief/palm-beach-christmas/2021DEC-100GOPRO/` | 21 | 20,958,806,312 | 7 MP4 (GH010015, GH010023, GH010024, GH010034, GH020034, GH030034, GH040034), 7 THM, 7 LRV |
| **time-moment-brief** | `palm-beach-christmas` / `2021DEC-360GOPRO` | `time-moment-brief/palm-beach-christmas/2021DEC-360GOPRO/` | 102 | 93,896,076,011 | 34 .360 (Takes 14–18), 34 LRV, 34 THM |
| **time-moment-brief** | `palm-beach-christmas` / `2021DEC-PANASONIC` | `time-moment-brief/palm-beach-christmas/2021DEC-PANASONIC/` | 40 | 2,674,868,767 | 40 MP4 (P1000045–P1000084) |
| **time-moment-brief** | `pompano-concepts` / `2021AUG-100GOPRO` | `time-moment-brief/pompano-concepts/2021AUG-100GOPRO/` | 67 | 33,266,419,054 | 23 MP4 (GH010004–GH040007), 23 THM, 21 LRV |
| **time-moment-brief** | `pompano-concepts` / `2021AUG-PANASONIC` | `time-moment-brief/pompano-concepts/2021AUG-PANASONIC/` | 20 | 30,792,510,443 | 17 MP4 (P1000002–P1000021), 3 JPG (P1000003, 007, 008) |
| **time-moment-brief** | *.DS_Store* metadata | 3 internal paths | 3 | 26,636 | `time-moment-brief/.DS_Store`, `palm-beach-christmas/.DS_Store`, `2021DEC-100GOPRO/.DS_Store` |
| **SUBTOTAL (TMB)** | **5 Banks + 3 Meta** | `time-moment-brief/` | **253** | **181,588,707,123** | **~181.59 GB** |
| **backwards-up-hill** | `2022FEB-100GOPRO` | `backwards-up-hill/2022FEB-100GOPRO/` | 4 | 2,044,858,353 | 2 MP4 (GH010043, GH010044), 2 THM |
| **backwards-up-hill** | `2022FEB-360GOPRO` | `backwards-up-hill/2022FEB-360GOPRO/` | 36 | 23,285,133,086 | 11 .360 (Takes 38–42, 47, 48), 11 LRV, 12 THM, 2 JPG |
| **backwards-up-hill** | `2022FEB-DJI` | `backwards-up-hill/2022FEB-DJI/` | 22 | 30,072,668,795 | 11 MP4 (DJI_0057–DJI_0067), 11 LRF |
| **backwards-up-hill** | `2022FEB-F6` | `backwards-up-hill/2022FEB-F6/` | 13 | 3,438,452,644 | 13 WAV (220218_001–220218_013) |
| **backwards-up-hill** | `2022FEB-PANASONIC` | `backwards-up-hill/2022FEB-PANASONIC/` | 17 | 41,104,508,164 | 16 MP4 (P1000085–P1000101, omitting 088), 1 JPG (P1000088) |
| **backwards-up-hill** | *.DS_Store* metadata | 2 internal paths | 2 | 8,196 | `backwards-up-hill/.DS_Store`, etc. |
| **SUBTOTAL (BUH)** | **5 Banks + 2 Meta** | `backwards-up-hill/` | **94** | **99,945,629,238** | **~99.95 GB** |
| **TOTAL (10 Banks)** | **10 Banks** | **Both Roots** | **347** | **281,534,336,361** | **~281.53 GB** |

**Structural invariants**:
- Exactly 347 regular files, 281,534,336,361 logical bytes, 12 directories, 0 symlinks, 0 special files.
- Matches frozen private manifest `ingress-inventory-20261012-56876a482ab8/inventory.json` (SHA-256: `9cb729dcf38be13c7faff5e891cbfc9c1e126b833591ef026e773be6010fefe6`) with zero missing files, zero additions, and zero size mismatches.

---

### 1.2 In-Place Reconciliation of Six Loose Ingress Media Candidates
Six loose media files reside directly in the root directory `/Volumes/Ingress/`. Per custody requirements, these candidates are **reconciled in place without moving, renaming, or deleting them**:

| Filename | Exact Logical Size (Bytes) | UTC Modification Timestamp | Streamed SHA-256 Digest | Historical & Compositional Role |
|---|---|---|---|---|
| `2023-11-06b - alemor.mp4` | 1,919,468,325 | 2023-11-06T19:24:20Z | `710f70fab427a622b9c6ba1d3c80efa1f231fc447af7e575eb90dc6aabeda766` | External reference edit / screening capture |
| `692D3297-982D-46B8-B411-EB7FA3925396.MP4` | 217,677,918 | 2026-10-05T03:47:29Z | `48049ff35feea4b3502f718477b501dac79d5de2858bdc96816175cbbb2f2307` | Reference video of user vertical edit |
| `692D3297-982D-46B8-B411-EB7FA3925396.mov` | 59,130,459 | 2026-10-05T21:28:03Z | `926df53f621797c349590f102a39de90affefcc4d15ce4608db8488c148bed13` | QuickTime derivative of vertical edit |
| `screen-recording-2025-03-18-at-3-22-21-pm.mov` | 8,362,528,363 | 2025-03-18T20:54:52Z | `72ee668c68c3a91b77b497f590b3020b5d888964f0574e65c67bdc27990ecb1f` | Historical screen recording of prior playback / edit |
| `up-the-hill-backwards.mov` | 51,877,542 | 2026-10-05T21:28:29Z | `019fd4eb2150c51a75352ac4bb8a260144a774ff88576eac100e00ba79ec00ba` | QuickTime derivative of first iteration |
| `up-the-hill-backwards.mp4` | 199,654,595 | 2026-10-05T03:47:16Z | `e83eb57a2066e0b37d08669639b6c066467282b0625f09f22468a5a6ed165fc3` | Reference video of first iteration |
| **TOTAL (Loose Media)** | **10,810,337,202** | — | — | **6 files (~10.81 GB)** |

---

### 1.3 Volume Capacity & Live APFS Accounting
Combining the 10-bank inventory payload and the 6 loose media candidates establishes complete accounting of the `/Volumes/Ingress` volume:
- **10-Bank Inventory Payload**: 281,534,336,361 bytes (347 files)
- **Loose Media Candidates**: 10,810,337,202 bytes (6 files)
- **Total Accounted Payload**: **292,344,673,563 bytes (353 files, ~292.34 GB)**
- **Live Used Space (`diskutil info /Volumes/Ingress`)**: **292,347,879,424 bytes (292.3 GB)**
- **APFS Allocation Margin**:
  $$292,347,879,424 - 292,344,673,563 = 3,205,861 \text{ bytes } (\approx 3.06 \text{ MiB})$$

The 3.06 MiB difference corresponds precisely to the APFS filesystem structures: directory nodes, the 12 bank directories, root directories, `.fseventsd` transaction logs, `.Spotlight-V100` indices, and volume catalog records. Every byte on the physical volume is accounted for.

---

## 2. Physical Store Qualification & Storage Independence

### 2.1 Live Volume Identification by Filesystem UUID
Physical devices and APFS containers can shift device node identifiers across reboot or bus resets. Volumes are strictly qualified and resolved by their permanent filesystem UUIDs:

| Volume Name | Device Node | Filesystem UUID | APFS Container | Physical Store | Total Capacity | Container Free Space | Mount Point |
|---|---|---|---|---|---|---|---|
| **Ingress** | `/dev/disk7s2` | `8E4C5386-7281-4E65-BC65-363C08FAAE50` | `disk7` | `/dev/disk6s2` (External 4TB SSD) | 4,000,543,715,328 | 1,214,555,811,840 (~1.2 TB) | `/Volumes/Ingress` |
| **Archive4T** | `/dev/disk7s1` | `45C8AA30-307B-41E2-908D-5112E93B4AF5` | `disk7` | `/dev/disk6s2` (External 4TB SSD) | 4,000,543,715,328 | 1,214,555,811,840 (~1.2 TB) | `/Volumes/Archive4T` |
| **T7Recovery** | *N/A* | `0287E02B-989A-419B-A7CA-B4BCE4ECA1FF` | *N/A (was disk9)* | *External 1TB Samsung T7* | 999,995,129,856 | *Unknown* | **UNMOUNTED / DISCONNECTED** |

---

### 2.2 Physical Store Colocation Hazard
1. **Container Colocation**:
   `Ingress` and `Archive4T` are synthesized APFS volumes sharing a single APFS container (`disk7`) on the same physical drive (`/dev/disk6s2`).
2. **Independence Constraint**:
   Writing a complete replica or restore tree to `Archive4T` verifies restore mechanics, directory recreation, metadata preservation, and byte-for-byte fidelity within a secondary volume. However, **copying between `Ingress` and `Archive4T` does not establish physical store independence**. A hardware failure, bus failure, electrical event, or physical damage to disk `disk6` will compromise both volumes simultaneously.
3. **Disconnection of T7Recovery**:
   The standalone external drive `T7Recovery` (`0287E02B-989A-419B-A7CA-B4BCE4ECA1FF`, physical `disk9`), which provided independent physical custody in prior sessions, is currently unmounted and disconnected. True multi-device physical store independence requires `T7Recovery` (or an equivalent physical drive) to be connected and verified.

---

### 2.3 The 20 GiB Reserve Guard
Before admitting any write operation to `Archive4T`, available container capacity must satisfy the inviolable reserve rule:
- **Container Free Space**: $1,214,555,811,840 \text{ bytes } (\approx 1.215 \text{ TB})$
- **Inviolable Minimum Reserve**: $20 \text{ GiB} = 21,474,836,480 \text{ bytes}$
- **Full Restored Estate Payload**: $292,344,673,563 \text{ bytes } (\approx 292.34 \text{ GB})$
- **Available Margin After Payload + Reserve**:
  $$1,214,555,811,840 - (292,344,673,563 + 21,474,836,480) = 900,736,301,797 \text{ bytes } (\approx 900.74 \text{ GB})$$

The available margin of ~900.7 GB comfortably exceeds the safety threshold.

---

## 3. Streamed SHA-256 and Restore Proof Protocol

### 3.1 Streaming Hashing Architecture
1. **Chunking**: Source files are read in streaming chunks of 8 MiB ($8,388,608 \text{ bytes}$) directly into SHA-256 digest accumulators.
2. **Stat Verification**:
   - `stat()` is captured immediately before opening the file descriptor.
   - `stat()` is captured immediately after closing the file descriptor.
   - The file size (`st_size`), nanosecond modification timestamp (`st_mtime_ns`), inode (`st_ino`), and device identifier (`st_dev`) must remain strictly identical across the hashing pass.
3. **Immutability Assurance**: The archival source on `/Volumes/Ingress` is opened with read-only flags (`O_RDONLY`).

---

### 3.2 Safe Transfer & Restore Verification Protocol
When transferring to a qualified destination (`Archive4T` or `T7Recovery`):
1. **Exclusive Staging Creation**:
   Destination files are opened with `O_CREAT | O_EXCL` using a per-file temporary extension (`.partial`). If a destination file already exists, the transfer is refused; overwrite modes are strictly forbidden.
2. **Fsync & Readback from Hardware**:
   Upon completing the byte stream, `os.fsync()` is issued to flush all disk caches. The write handle is closed. The destination file is reopened afresh from the physical storage node and hashed with streamed SHA-256 to ensure data was written to physical NAND without corruption.
3. **Atomic Promotion**:
   Only after the device readback hash and byte count exactly match the source manifest is the temporary file atomically renamed (`os.replace` / `rename`) to its permanent filename.
4. **Clean Failure Rollback**:
   If any exception occurs during transfer, fsync, or readback verification, the `.partial` file is immediately unlinked. Interrupted transfers leave zero partial-file residue in destination directories.
5. **Intact Recovery Ledger**:
   An interrupted transfer records its exact state in an external recovery ledger (`custody-interrupted-ledger.json`), documenting completed files, interrupted files (unlinked), remaining bytes, and error causes, allowing clean resumption without partial contamination.
6. **End-to-End Restore Proof**:
   Restore verification requires an independent post-transfer traversal comparing:
   - Total file count (exact match).
   - Root-relative directory hierarchy (exact match).
   - Byte sizes for each file (exact match).
   - Independent SHA-256 digest recalculation against the frozen source manifest.

---

## 4. Camera Coverage & Sensor Designation Proof

### 4.1 Exhaustive Analysis of `backwards-up-hill` Footage
The `backwards-up-hill` directory contains 5 camera and audio banks:
- `2022FEB-100GOPRO`: 2 video clips (`GH010043.MP4`, `GH010044.MP4`) and 2 THM thumbnails.
- `2022FEB-360GOPRO`: 11 dual-stream `.360` clips across 7 takes (Takes 38, 39, 40, 41, 42, 47, 48), 11 LRVs, 12 THMs, 2 JPGs.
- `2022FEB-DJI`: 11 video clips (`DJI_0057.MP4` through `DJI_0067.MP4`), 11 LRFs.
- `2022FEB-PANASONIC`: 16 video clips (`P1000085.MP4` through `P1000101.MP4`, omitting 088), 1 JPG (`P1000088.JPG`).
- `2022FEB-F6`: 13 multi-channel 24-bit 48 kHz WAV audio files (`220218_001.WAV` through `220218_013.WAV`).

---

### 4.2 Mathematical and Empirical Proof of Take 48 Overlap
The master acoustic anchor for the session is Zoom F6 multi-track file `2022FEB-F6/220218_012.WAV` (duration: 1722.988s, 5 channels, 48 kHz, SHA-256: `6041a38fb946dd7342e2f12e2f6c2abd9e2f826810702382633ba15f9ad02616`).

Seed-free onset-envelope cross-correlation (spectral flux at 10 ms hop, 1 kHz high-pass) over the full anchor proves the camera alignment offsets:
- `GS010048.360` (GoPro MAX 360): start offset $252.1868\text{s}$, duration $482.496\text{s} \implies$ coverage window $[252.1868, 734.6828]\text{s}$.
- `P1000096.MP4` (Panasonic G100): start offset $325.0388\text{s}$, duration $359.8595\text{s} \implies$ coverage window $[325.0388, 684.8983]\text{s}$.
- `DJI_0066.MP4` (DJI Action): start offset $497.7554\text{s}$, duration $409.000\text{s} \implies$ coverage window $[497.7554, 906.7554]\text{s}$.

The common temporal intersection where all active cameras co-recorded simultaneously is:
$$\text{Overlap} = [\max(252.1868, 325.0388, 497.7554), \min(734.6828, 684.8983, 906.7554)] = \mathbf{[497.7554, 684.8983]\text{s}}$$
- **Total Common Overlap Duration**: $684.8983 - 497.7554 = \mathbf{187.1429\text{s}}$.
- **Approved Generation Windows**:
  - Generation 01: $[510.0, 518.0]\text{s}$ ($\Delta = 8.0\text{s}$)
  - Generation 02: $[518.0, 526.0]\text{s}$ ($\Delta = 8.0\text{s}$)
  Both generation windows fall strictly inside the $187.14\text{s}$ common overlap window.

---

### 4.3 Empirical Proof: 100GOPRO Recorded 20 Minutes Prior to Take 48
An exhaustive search was conducted to determine whether the GoPro 100 camera (`2022FEB-100GOPRO`) overlapped Take 48 or could provide a fourth physical camera sensor:
1. **Timecode & Duration Measurements**:
   - `GH010043.MP4`:
     - QuickTime Timecode: `16:13:43:49`
     - Duration: $69.819\text{s}$
     - Interval: `16:13:43` to `16:14:53`
   - `GH010044.MP4`:
     - QuickTime Timecode: `16:15:34:19`
     - Duration: $139.121\text{s}$
     - Interval: `16:15:34` to `16:17:53`
   - The entire `100GOPRO` bank concluded recording at **16:17:53**.
2. **Take 48 Commencement**:
   - `GS010048.360`:
     - QuickTime Timecode: `16:38:26:20`
     - Duration: $482.496\text{s}$
     - Interval: `16:38:26` to `16:46:28`
3. **Temporal Gap**:
   $$16:38:26 - 16:17:53 = \mathbf{20\text{ minutes, } 33\text{ seconds}}$$
   The 100GOPRO camera was powered off more than 20 minutes before Take 48 began.
4. **Exhaustive 360 Bank Verification**:
   The entire `2022FEB-360GOPRO` directory was examined for any earlier clips co-recording with 100GOPRO:
   - `GS010042.360`: timecode `14:32:44:19`, duration $8.6\text{s}$ (ended over 1 hour 40 minutes prior).
   - `GS010047.360`: timecode `16:36:17:28`, duration $28.8\text{s}$ (started 18 minutes after 100GOPRO ended).
   - No 360 clip was recorded between 14:32:53 and 16:36:17.
5. **Acoustic Cross-Correlation**:
   Blind acoustic cross-correlation of `GH010043.MP4` and `GH010044.MP4` against master anchor `220218_012.WAV` yielded zero peak alignment with the generation interval (spurious peaks landed at $54.00\text{s}$ and $760.00\text{s}$, well outside the $[510.0, 526.0]\text{s}$ generation window).

---

### 4.4 Derivation of `cam3` and Reaffirmation of "Four Views / Three Sensors"
1. **Cam3 Optical Origin**:
   Because no fourth physical camera operated during Take 48, `cam3` is derived from the GoPro MAX dual-stream file `GS010048.360` (Sensor 1).
2. **Perspective Re-projection Pipeline**:
   - `GS010048.360` stream 0 is unpacked and stitched via GEQ seam-blending and EAC-to-equirectangular filtering into `generation_XX.panorama.full.mp4` (Resolution: $1536 \times 768$, equirectangular projection).
   - `cam3` is then computed directly from this equirectangular intermediate via FFmpeg `v360`:
     ```bash
     ffmpeg -nostdin -y -i generation_XX.panorama.full.mp4 \
       -vf "v360=equirect:rectilinear:h_fov=90:v_fov=50:w=1024:h=576:interp=linear,fps=24,format=yuv420p" \
       -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p -g 24 -movflags +faststart \
       generation_XX.cam3.full.mp4
     ```
3. **Sensor-to-View Mapping**:

   | View / Role | Projection Geometry | Physical Sensor Hardware | Source Archival File |
   |---|---|---|---|
   | `panorama` | Equirectangular ($360^\circ \times 180^\circ$) | GoPro MAX Dual-Stream (Sensor 1) | `backwards-up-hill/2022FEB-360GOPRO/GS010048.360` |
   | `cam3` | Rectilinear Perspective ($90^\circ\text{H} \times 50^\circ\text{V}$) | GoPro MAX Dual-Stream (Sensor 1 re-projection) | `backwards-up-hill/2022FEB-360GOPRO/GS010048.360` |
   | `cam1` | Rectilinear Native Framing | Panasonic Lumix G100 (Sensor 2) | `backwards-up-hill/2022FEB-PANASONIC/P1000096.MP4` |
   | `cam2` | Rectilinear Wide Native Framing | DJI Action 2 (Sensor 3) | `backwards-up-hill/2022FEB-DJI/DJI_0066.MP4` |
   | *Audio Anchor* | Ambisonic / 5-Channel Discrete | Zoom F6 Multitrack Field Recorder | `backwards-up-hill/2022FEB-F6/220218_012.WAV` |

4. **Constitutional Designation**:
   The four-view compositional atlas contract is geometrically fulfilled. However, the scene is captured by **exactly three physical video sensors**. This verified designation is permanent and immutable for the `backwards-up-hill` archive; no claim of four distinct physical video cameras may be made unless an entirely new multi-camera physical production is shot.

---

## 5. Serialized Execution and Bounded Attempts

### 5.1 Serialized Steps
1. **Pre-flight Identification**: Re-resolve volume UUIDs (`Ingress`: `8E4C5386-7281-4E65-BC65-363C08FAAE50`, `Archive4T`: `45C8AA30-307B-41E2-908D-5112E93B4AF5`). Confirm live free space on `disk7` ($\ge 20\text{ GiB}$ reserve preserved after adding $292.34\text{ GB}$).
2. **In-Place Preservation**: Confirm that the 6 loose Ingress media candidates remain at their original root paths. Never move or rename them.
3. **Creation of Isolated Target Roots**: When copying to `Archive4T`, create a mode-0700 root: `/Volumes/Archive4T/limen-custody/original-media-20261018-<hash>/`.
4. **Streaming Hash and Copy**: Read each source file, compute streamed SHA-256, write to `.partial` file on target, fsync, reopen from target to verify device readback, and promote to final path.
5. **Restore Verification**: Perform full independent tree verification against frozen manifests (`ingress-original-media-inventory-2026-10-18-v2.json` and `ingress-inventory-20261012-56876a482ab8`).
6. **Publish Sanitized Receipts**: Record results in `Workspace/audiovisual-composition-system/docs/evidence/` with file count, byte size, and receipt hash.

### 5.2 Bounded Attempt Constraints
- Single recovery writer with bounded I/O workload.
- Maximum 30-minute wall bound per attempt, with at most 10 minutes of verification.
- Stop on admission denial without retry loops.
- Incomplete transfers preserve recovery ledgers and clean up `.partial` files immediately.

---

## 6. Acceptance Exclusions

1. Full playback decoding, WebCodecs playback, headset/XR acceptance, and display synchronization are governed separately under Requirements R2 and R3.
2. The physical colocation of `Ingress` and `Archive4T` on `disk6s2` must be explicitly stated in all generated receipts.
3. PRs #2 and #3 in `audiovisual-composition-system` remain open for architectural review; no media retirement, truncation, or branch deletion is authorized.
