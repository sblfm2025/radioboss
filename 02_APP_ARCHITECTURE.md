# 02 — App Architecture

## Rekomendasi Teknologi

Gunakan salah satu stack berikut:

### Pilihan Utama

```text
Python + PySide6 + SQLite
```

Alasan:

- cocok untuk desktop Windows,
- ringan,
- mudah scan filesystem,
- mudah baca/tulis CSV/JSON/M3U8,
- mudah dibuat installer,
- cocok untuk PC studio.

### Alternatif

```text
Tauri + React + Rust backend
```

Gunakan hanya jika developer terbiasa dengan Rust/Tauri.

## Struktur Project

```text
radioboss_fresh_reset_manager/
├── app.py
├── requirements.txt
├── config/
│   ├── app_config.json
│   ├── scan_rules.json
│   ├── keyword_rules.json
│   ├── folder_structure.json
│   ├── clock_templates.json
│   └── scheduler_templates.json
│
├── core/
│   ├── scanner.py
│   ├── file_indexer.py
│   ├── playlist_parser.py
│   ├── playlist_auditor.py
│   ├── classifier.py
│   ├── danger_detector.py
│   ├── backup_manager.py
│   ├── fresh_folder_builder.py
│   ├── copy_manager.py
│   ├── m3u8_generator.py
│   ├── clock_builder.py
│   ├── scheduler_plan_builder.py
│   ├── live_source_manager.py
│   ├── emergency_fallback_builder.py
│   ├── report_writer.py
│   └── manifest_writer.py
│
├── db/
│   ├── database.py
│   └── schema.sql
│
├── ui/
│   ├── main_window.py
│   ├── dashboard_page.py
│   ├── drive_scan_page.py
│   ├── playlist_audit_page.py
│   ├── classification_page.py
│   ├── fresh_structure_page.py
│   ├── playlist_builder_page.py
│   ├── scheduler_plan_page.py
│   ├── live_source_page.py
│   ├── reports_page.py
│   └── settings_page.py
│
├── output/
│   ├── reports/
│   ├── manifests/
│   ├── playlists/
│   ├── scheduler_plan/
│   └── logs/
│
└── tests/
    ├── test_playlist_parser.py
    ├── test_classifier.py
    ├── test_danger_detector.py
    └── test_m3u8_generator.py
```

## Data Flow

```text
Drive/Folder Scan
    ↓
File Index SQLite
    ↓
Classification + Danger Detection
    ↓
Playlist Audit
    ↓
Cleanup Plan
    ↓
Fresh Folder Build
    ↓
Copy Approved Files
    ↓
Playlist/Clock Generation
    ↓
Scheduler Plan
    ↓
Reports + Manifest
```

## Core Entities

### FileItem

```python
@dataclass
class FileItem:
    id: str
    original_path: str
    file_name: str
    extension: str
    size_bytes: int
    modified_at: str
    detected_type: str | None
    risk_level: str
    status: str
    recommended_folder: str | None
    notes: str | None
```

### Playlist

```python
@dataclass
class Playlist:
    id: str
    path: str
    name: str
    total_items: int
    missing_items: int
    dangerous_items: int
    status: str
    recommendation: str
```

### ClockTemplate

```python
@dataclass
class ClockTemplate:
    id: str
    name: str
    start_time: str
    end_time: str
    allowed_categories: list[str]
    blocked_tags: list[str]
    insert_rules: list[dict]
    fallback_playlist: str | None
```

### LiveSourcePlan

```python
@dataclass
class LiveSourcePlan:
    id: str
    type: str
    title: str
    date: str
    start_time: str
    end_time: str
    source_url: str | None
    audio_route: str | None
    fallback_playlist: str
    checklist_status: str
```

## Logging

Setiap aksi penting harus dicatat:

```text
logs/app.log
logs/scan.log
logs/copy.log
logs/export.log
logs/error.log
```

Format minimal:

```text
timestamp | level | module | message | related_path
```

## Error Handling

- File tidak bisa dibaca → tandai `READ_ERROR`, jangan hentikan scan.
- Path terlalu panjang → tandai `PATH_TOO_LONG`.
- Permission error → tandai `PERMISSION_DENIED`.
- File duplikat → masuk report, jangan hapus.
- Playlist rusak → parse sebagian jika memungkinkan, lalu beri status `BROKEN_PLAYLIST`.

## Konfigurasi Awal

`config/app_config.json`:

```json
{
  "freshRoot": "D:\\RADIO_SBL_FRESH",
  "defaultAction": "copy",
  "allowDelete": false,
  "allowOverwrite": false,
  "scanMode": "maintenance",
  "databasePath": "db\\radioboss_fresh_reset.sqlite"
}
```
