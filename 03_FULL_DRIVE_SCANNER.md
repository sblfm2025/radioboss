# 03 — Full Drive Scanner

## Tujuan

Fitur scan drive penuh untuk menemukan semua aset RadioBOSS dan aset siaran yang tersebar di PC.

Karena RadioBOSS akan dihentikan sementara, mode utama adalah:

```text
Fresh Reset Maintenance Scan
```

Tetap pastikan scan tidak merusak file.

## Input UI

```text
Pilih Drive / Folder:
[ ] C:\
[ ] D:\
[ ] E:\
[Browse Folder]

Mode:
( ) Audit Only
(✓) Fresh Reset Maintenance
( ) Deep Audit With Metadata

Opsi:
[✓] Skip folder sistem
[✓] Skip recycle bin
[✓] Skip node_modules/.git/cache/temp
[✓] Simpan hasil ke SQLite
[✓] Jangan ubah file saat scan
[✓] Baca metadata audio pada Deep Audit
```

## Ekstensi yang Diproses

### Audio

```text
.mp3
.wav
.flac
.m4a
.aac
.ogg
.wma
```

### Playlist

```text
.m3u
.m3u8
.pls
```

### Pendukung Jika Relevan

```text
.txt
.csv
.json
.xml
.ini
.bak
```

File pendukung hanya diproses jika:

- nama/path mengandung `radioboss`, `playlist`, `jadwal`, `schedule`, `radio`, `ramadhan`, `adzan`, `iklan`, `ilm`, `jingle`, `podcast`, `event`, atau
- ukuran file di bawah 20 MB.

## Folder yang Harus Dilewati

```text
C:\Windows
C:\Program Files selain folder RadioBOSS
C:\Program Files (x86) selain folder RadioBOSS
C:\ProgramData\Microsoft
C:\$Recycle.Bin
C:\System Volume Information
node_modules
.git
.cache
cache
temp
tmp
```

## Tahap Scan

### Tahap 1 — File Indexing

Catat metadata filesystem saja:

```text
- path
- file_name
- extension
- size_bytes
- modified_at
- parent_folder
- drive
```

Jangan klasifikasi kompleks pada tahap ini.

### Tahap 2 — Keyword Classification

Klasifikasi awal dari nama file dan path.

### Tahap 3 — Playlist Parsing

Baca `.m3u`, `.m3u8`, `.pls`.

Periksa:

- total item,
- path ada/tidak,
- path relatif/absolut,
- item Ramadhan/adzan/iklan/ILM/jingle,
- item mengarah folder lama,
- item mengarah folder review/cache/download.

### Tahap 4 — Metadata Audio Optional

Baca metadata hanya pada mode Deep Audit:

- title,
- artist,
- album,
- duration,
- bitrate jika tersedia.

Jika metadata error, jangan gagal. Tandai `METADATA_ERROR`.

## Output Database

Tabel `files_index` harus berisi semua temuan.

Kolom minimal:

```text
id
path
file_name
extension
size_bytes
modified_at
parent_folder
detected_type
risk_level
status
recommended_folder
scan_batch_id
```

## Output Report

```text
output/reports/drive_scan_summary.csv
output/reports/all_audio_candidates.csv
output/reports/playlist_files_found.csv
output/reports/suspicious_files.csv
output/reports/folder_map.csv
```

## Level Risiko Scan

```text
LOW      = aset biasa, tidak berbahaya
MEDIUM   = perlu review, misalnya ILM tanpa tanggal
HIGH     = adzan/ramadhan ditemukan di lokasi umum
CRITICAL = playlist aktif/kemungkinan aktif memuat adzan/ramadhan/broken path
```

## Pseudocode

```python
def scan_drive(root_paths, config):
    batch_id = create_scan_batch()
    for root in root_paths:
        for current_dir, dirs, files in os.walk(root):
            dirs[:] = filter_allowed_dirs(dirs)
            for name in files:
                path = Path(current_dir) / name
                if not is_relevant_extension(path):
                    continue
                record = build_file_record(path, batch_id)
                save_file_index(record)
    classify_indexed_files(batch_id)
    parse_playlists(batch_id)
    generate_scan_reports(batch_id)
```

## Acceptance Criteria

- Bisa scan drive penuh tanpa crash.
- File yang tidak bisa dibaca tidak menghentikan scan.
- Hasil tersimpan ke SQLite.
- Ada progress UI.
- Ada tombol pause/stop.
- Tidak ada file yang diubah pada mode scan.
- Laporan bisa diekspor CSV.
