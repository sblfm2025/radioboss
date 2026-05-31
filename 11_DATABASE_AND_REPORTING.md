# 11 — Database and Reporting

## Database

Gunakan SQLite lokal.

File default:

```text
db\radioboss_fresh_reset.sqlite
```

## Schema Minimal

```sql
CREATE TABLE scan_batches (
  id TEXT PRIMARY KEY,
  started_at TEXT,
  finished_at TEXT,
  mode TEXT,
  root_paths TEXT,
  status TEXT
);

CREATE TABLE files_index (
  id TEXT PRIMARY KEY,
  scan_batch_id TEXT,
  path TEXT,
  file_name TEXT,
  extension TEXT,
  size_bytes INTEGER,
  modified_at TEXT,
  parent_folder TEXT,
  detected_type TEXT,
  risk_level TEXT,
  status TEXT,
  recommended_folder TEXT,
  notes TEXT
);

CREATE TABLE playlists (
  id TEXT PRIMARY KEY,
  scan_batch_id TEXT,
  file_path TEXT,
  file_name TEXT,
  total_items INTEGER,
  missing_items INTEGER,
  dangerous_items INTEGER,
  status TEXT,
  recommendation TEXT
);

CREATE TABLE playlist_items (
  id TEXT PRIMARY KEY,
  playlist_id TEXT,
  item_path TEXT,
  exists_on_disk INTEGER,
  detected_type TEXT,
  danger_tag TEXT,
  risk_level TEXT,
  recommendation TEXT
);

CREATE TABLE copy_actions (
  id TEXT PRIMARY KEY,
  source_path TEXT,
  target_path TEXT,
  action TEXT,
  status TEXT,
  error_message TEXT,
  created_at TEXT
);

CREATE TABLE clock_templates (
  id TEXT PRIMARY KEY,
  name TEXT,
  start_time TEXT,
  end_time TEXT,
  allowed_categories TEXT,
  blocked_tags TEXT,
  insert_rules TEXT,
  fallback_playlist TEXT
);

CREATE TABLE exports (
  id TEXT PRIMARY KEY,
  export_date TEXT,
  export_type TEXT,
  file_path TEXT,
  manifest_path TEXT,
  status TEXT,
  created_at TEXT
);

CREATE TABLE live_source_plans (
  id TEXT PRIMARY KEY,
  type TEXT,
  title TEXT,
  date TEXT,
  start_time TEXT,
  end_time TEXT,
  source_url TEXT,
  audio_route TEXT,
  fallback_playlist TEXT,
  status TEXT
);
```

## Required Reports

```text
10_LAPORAN_RESET\CSV\drive_scan_summary.csv
10_LAPORAN_RESET\CSV\all_audio_candidates.csv
10_LAPORAN_RESET\CSV\playlist_files_found.csv
10_LAPORAN_RESET\CSV\playlist_lama_report.csv
10_LAPORAN_RESET\CSV\playlist_items_detail.csv
10_LAPORAN_RESET\CSV\dangerous_items.csv
10_LAPORAN_RESET\CSV\ramadhan_adzan_report.csv
10_LAPORAN_RESET\CSV\expired_ads_report.csv
10_LAPORAN_RESET\CSV\podcast_report.csv
10_LAPORAN_RESET\CSV\special_event_report.csv
10_LAPORAN_RESET\CSV\live_source_plan.csv
10_LAPORAN_RESET\CSV\emergency_fallback_report.csv
10_LAPORAN_RESET\CSV\copy_manifest.csv
10_LAPORAN_RESET\CSV\copy_conflicts.csv
10_LAPORAN_RESET\CSV\scheduler_plan.csv
```

## Manifest Files

```text
10_LAPORAN_RESET\JSON\scan_manifest.json
10_LAPORAN_RESET\JSON\folder_structure_manifest.json
10_LAPORAN_RESET\JSON\export_manifest.json
10_LAPORAN_RESET\JSON\emergency_fallback_manifest.json
```

## HTML Summary

Buat `reset_summary.html` yang menampilkan:

```text
- total file discan
- total playlist lama
- total dangerous playlist
- total Ramadhan/adzan ditemukan
- total missing path
- total file copied
- total playlist baru
- total fallback ready
- daftar critical warnings
```

## Final Checklist

Buat `final_setup_checklist.md`:

```markdown
# Final Setup Checklist RadioBOSS

- [ ] Semua playlist lama sudah diarsipkan.
- [ ] Event Ramadhan lama sudah dinonaktifkan manual di RadioBOSS.
- [ ] Folder fresh sudah dibuat.
- [ ] File approved sudah dicopy.
- [ ] Playlist baru sudah dibuat.
- [ ] Playlist reguler bebas Ramadhan/adzan.
- [ ] Emergency fallback sudah siap.
- [ ] Scheduler plan sudah diinput manual ke RadioBOSS.
- [ ] Test playback semua clock berhasil.
- [ ] Operator memahami struktur baru.
```

## Acceptance Criteria

- Semua laporan bisa diekspor.
- Laporan tidak kosong jika ada data.
- Semua aksi copy tercatat.
- Semua playlist export punya manifest.
- Final checklist dibuat otomatis.
