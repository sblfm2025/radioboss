# 14 — Developer Prompt for Gemini / Codex

Gunakan prompt ini untuk memulai implementasi di Gemini/Codex.

---

## Prompt Utama

Anda adalah senior desktop application developer. Bangun aplikasi lokal Windows bernama **RadioBOSS Fresh Reset Manager**.

Aplikasi ini bertugas membantu reset fresh RadioBOSS untuk radio lokal. RadioBOSS akan dihentikan sementara saat proses reset, sehingga aplikasi boleh melakukan full drive scan, deep audit, copy file terkontrol, generate folder fresh, generate playlist `.m3u8`, dan generate scheduler plan. Namun aplikasi tidak boleh menghapus file lama permanen, tidak boleh overwrite konfigurasi RadioBOSS, dan tidak boleh melakukan aksi destruktif tanpa approval.

Gunakan stack:

```text
Python + PySide6 + SQLite
```

Buat struktur project:

```text
radioboss_fresh_reset_manager/
├── app.py
├── requirements.txt
├── config/
├── core/
├── db/
├── ui/
├── output/
└── tests/
```

Fitur MVP wajib:

1. **Drive Scanner**
   - Pilih drive/folder.
   - Scan ekstensi audio dan playlist.
   - Skip folder sistem/cache/node_modules/.git.
   - Simpan hasil ke SQLite.
   - Export `drive_scan_summary.csv`.

2. **Classification and Danger Detection**
   - Deteksi Ramadhan-only, adzan, imsak, sahur, takbiran, jingle, sweeper, ILM, iklan, podcast, special event, liputan, live source.
   - Beri risk level: LOW, MEDIUM, HIGH, CRITICAL.
   - Beri status: APPROVED, REVIEW, BLOCK_REGULAR, ADZAN_EVENT_ONLY, ARCHIVE_RECOMMENDED.

3. **Playlist Auditor**
   - Parse `.m3u`, `.m3u8`, `.pls`.
   - Deteksi missing paths.
   - Deteksi dangerous items.
   - Export `playlist_lama_report.csv` dan `playlist_items_detail.csv`.

4. **Fresh Folder Builder**
   - Buat struktur `D:\RADIO_SBL_FRESH` lengkap.
   - Jangan overwrite file existing.
   - Buat `folder_structure_manifest.json`.

5. **Copy Approved Files**
   - Default copy, bukan move.
   - Catat semua copy ke `copy_manifest.csv`.
   - Konflik nama file masuk `copy_conflicts.csv`.

6. **Playlist Builder**
   - Generate `.m3u8` per clock.
   - Validasi agar playlist reguler bebas Ramadhan/adzan/podcast/event/review.
   - Buat `export_manifest.json`.

7. **Scheduler Plan Builder**
   - Generate `scheduler_plan.csv`.
   - Generate `setup_scheduler_manual.md`.
   - Jangan tulis langsung ke konfigurasi RadioBOSS pada versi awal.

8. **Live Source and Emergency Fallback**
   - Buat data plan untuk YouTube relay, WhatsApp call, Zoom, Discord, Google Meet.
   - Setiap live source wajib punya audio routing profile dan fallback playlist.
   - Generate `live_source_plan.csv` dan `emergency_fallback_report.csv`.

9. **Reports**
   - CSV, JSON, HTML summary, dan final checklist MD.

UI wajib:

```text
Dashboard
Drive Scanner
Playlist Audit
Classification Review
Fresh Structure
Playlist Builder
Scheduler Plan
Special Programs
Live Source Tools
Emergency Fallback
Reports
Settings
```

Safety rules:

- Tidak ada delete permanen pada versi awal.
- Tidak ada auto overwrite.
- Semua aksi copy/generate butuh preview.
- File ragu-ragu masuk REVIEW.
- Adzan hanya event-only.
- Ramadhan-only tidak boleh masuk reguler.
- Podcast/event/liputan tidak boleh masuk playlist musik reguler.
- Live source wajib fallback.

Deliverables awal:

```text
- project skeleton
- SQLite schema
- drive scanner working
- classifier working
- playlist parser working
- CSV report writer working
- PySide6 UI minimal
```

Tulis kode modular, jelas, dan mudah diuji. Sertakan unit test untuk parser playlist, classifier, danger detector, dan m3u8 generator.

---

## Prompt Lanjutan untuk Modul Playlist Parser

Implementasikan `core/playlist_parser.py`.

Requirements:

- Mendukung `.m3u`, `.m3u8`, `.pls`.
- Abaikan baris komentar `#EXTM3U`, `#EXTINF`, dan baris kosong.
- Ambil path audio dari playlist.
- Resolve relative path berdasarkan folder playlist.
- Cek apakah file target ada.
- Return list item dengan field:

```python
{
  "raw_line": str,
  "resolved_path": str,
  "exists": bool,
  "extension": str,
  "detected_type": str | None,
  "risk_level": str | None
}
```

Jangan crash jika file playlist encoding berbeda. Coba `utf-8`, lalu `latin-1`.

---

## Prompt Lanjutan untuk Classifier

Implementasikan `core/classifier.py` dan `core/danger_detector.py`.

Rules:

- Klasifikasi berdasarkan path lowercase dan filename lowercase.
- Keyword rules dibaca dari `config/keyword_rules.json`.
- Jika keyword Ramadhan ditemukan → `detected_type=ramadhan_only`, `status=BLOCK_REGULAR`, `risk=HIGH`.
- Jika keyword adzan/waktu shalat ditemukan → `detected_type=adzan`, `status=ADZAN_EVENT_ONLY`, `risk=HIGH`.
- Jika podcast/event/liputan ditemukan → blocked from regular.
- Jika tidak jelas → REVIEW.

Buat unit test untuk semua kategori utama.

---

## Prompt Lanjutan untuk UI

Implementasikan UI PySide6 minimal dengan sidebar dan halaman:

- Dashboard
- Drive Scanner
- Playlist Audit
- Reports
- Settings

Dashboard menampilkan summary dari database.
Drive Scanner punya tombol pilih folder, start scan, stop scan, progress, dan table hasil.
Reports menampilkan daftar CSV/JSON/HTML yang sudah dibuat.

Jangan buat UI rumit dulu. Fokus fungsi utama berjalan stabil.
