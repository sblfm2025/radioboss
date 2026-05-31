# 12 — UI/UX Requirements

## Karakter UI

Aplikasi desktop harus sederhana, jelas, dan tidak membingungkan operator.

Gunakan gaya:

```text
- layout bersih,
- sidebar modul,
- status badge jelas,
- tombol aksi besar,
- progress scan terlihat,
- tabel bisa filter/search,
- warning kritis mudah terlihat.
```

## Menu Utama

```text
Dashboard
Drive Scanner
Playlist Audit
Classification Review
Fresh Structure
Copy/Build Plan
Playlist Builder
Scheduler Plan
Special Programs
Live Source Tools
Emergency Fallback
Reports
Settings
```

## Dashboard

Tampilkan kartu:

```text
- Total file discan
- Total playlist ditemukan
- Playlist dangerous
- Ramadhan/adzan detected
- Missing paths
- File ready copy
- Playlist baru ready
- Fallback ready
```

CTA utama:

```text
Start Fresh Reset Scan
Open Latest Report
Build Fresh Structure
Generate Playlists
```

## Drive Scanner Page

Komponen:

```text
- pilih drive/folder
- pilih mode scan
- progress bar
- current file
- elapsed time
- stop/pause button
- summary live
```

## Playlist Audit Page

Tabel kolom:

```text
Playlist
Total Item
Missing
Ramadhan
Adzan
Podcast/Event
Risk
Status
Recommendation
```

Filter:

```text
All
Dangerous
Broken
Safe Reference
Archive Only
```

## Classification Review Page

Tabel kolom:

```text
File
Detected Type
Risk
Status
Recommended Folder
Action
```

Aksi:

```text
Approve
Move to Review
Block Regular
Change Category
```

## Fresh Structure Page

Tampilkan tree struktur folder baru dan tombol:

```text
Build Fresh Structure
Open Fresh Root
Export Folder Manifest
```

## Playlist Builder Page

Fitur:

```text
- pilih tanggal
- pilih clock
- generate preview
- validate blocked tags
- export m3u8
```

## Scheduler Plan Page

Fitur:

```text
- daftar event baru
- target playlist
- status ready/not ready
- export CSV
- export manual setup MD
```

## Live Source Tools

Sub-tab:

```text
Relay YouTube
External Stream
WhatsApp Call
Zoom/Discord/Meet
Audio Routing Profiles
```

Wajib ada checklist per item.

## Emergency Fallback Page

Tabel:

```text
Fallback ID
Playlist File
Total Items
Duration Estimate
Danger Items
Status
```

## Reports Page

Daftar file laporan dengan tombol:

```text
Open
Export
Copy Path
```

## Status Badge

```text
READY = hijau
REVIEW = kuning
DANGEROUS = merah
CRITICAL = merah tebal
ARCHIVE = abu-abu
NOT_READY = oranye
```

## Acceptance Criteria

- Operator bisa memahami status tanpa membaca kode.
- Semua aksi berisiko butuh konfirmasi.
- Tidak ada tombol delete permanen pada versi awal.
- Semua warning kritis muncul di dashboard.
- Semua laporan bisa dibuka dari UI.
