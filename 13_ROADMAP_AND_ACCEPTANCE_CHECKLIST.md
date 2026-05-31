# 13 — Roadmap and Acceptance Checklist

## Roadmap Versi

### v0.1 — Full Drive Scanner

Target:

- Pilih drive/folder.
- Scan file relevan.
- Simpan ke SQLite.
- Export scan summary.

Acceptance:

```text
[ ] Scan drive berhasil.
[ ] File tidak relevan diskip.
[ ] Tidak ada file diubah.
[ ] Report drive_scan_summary.csv dibuat.
```

### v0.2 — Classification and Danger Detection

Target:

- Keyword classification.
- Detect Ramadhan/adzan/ILM/iklan/jingle/podcast/event.
- Risk scoring.

Acceptance:

```text
[ ] Ramadhan-only ditandai BLOCK_REGULAR.
[ ] Adzan ditandai ADZAN_EVENT_ONLY.
[ ] Podcast/event ditandai blocked from regular.
[ ] dangerous_items.csv dibuat.
```

### v0.3 — Playlist Auditor

Target:

- Parse `.m3u`, `.m3u8`, `.pls`.
- Detect missing path dan dangerous item.

Acceptance:

```text
[ ] playlist_lama_report.csv dibuat.
[ ] Playlist dangerous terdeteksi.
[ ] Missing path terdeteksi.
```

### v0.4 — Fresh Folder Builder

Target:

- Build struktur `D:\RADIO_SBL_FRESH`.
- Generate folder manifest.

Acceptance:

```text
[ ] Semua folder dibuat.
[ ] Tidak overwrite file.
[ ] folder_structure_manifest.json dibuat.
```

### v0.5 — Copy Approved Files

Target:

- Copy file approved ke folder rekomendasi.
- Conflict handling.

Acceptance:

```text
[ ] File asli tetap ada.
[ ] copy_manifest.csv dibuat.
[ ] copy_conflicts.csv dibuat bila ada konflik.
```

### v0.6 — Playlist Builder

Target:

- Generate `.m3u8` per clock.
- Validate blocked tags.

Acceptance:

```text
[ ] Playlist reguler bebas Ramadhan/adzan.
[ ] Manifest export dibuat.
[ ] File .m3u8 bisa dibuka RadioBOSS.
```

### v0.7 — Scheduler Plan Builder

Target:

- Generate scheduler_plan.csv.
- Generate setup_scheduler_manual.md.

Acceptance:

```text
[ ] Semua clock punya event plan.
[ ] Semua target file ada.
[ ] Tidak ada event reguler yang mengarah ke dangerous item.
```

### v0.8 — Special Program and Podcast Tools

Target:

- Manage podcast/event/liputan/lagu khusus.

Acceptance:

```text
[ ] Podcast tidak masuk playlist reguler.
[ ] Event punya manifest.
[ ] Lagu khusus hanya masuk event/special playlist.
```

### v0.9 — Live Source and Emergency Fallback

Target:

- YouTube relay plan.
- WhatsApp/Zoom/Discord plan.
- Emergency fallback builder.

Acceptance:

```text
[ ] Semua live source punya fallback.
[ ] Semua live source punya checklist.
[ ] Emergency fallback READY.
```

### v1.0 — Stable Fresh Reset Workflow

Target:

- End-to-end workflow.
- Final report.
- Final checklist.

Acceptance:

```text
[ ] Scan → classify → audit → build → copy → playlist → scheduler plan selesai.
[ ] reset_summary.html dibuat.
[ ] final_setup_checklist.md dibuat.
[ ] Tidak ada aksi destruktif default.
```

## Final Acceptance Checklist

```text
[ ] Aplikasi bisa scan drive penuh.
[ ] Aplikasi bisa menemukan playlist lama.
[ ] Aplikasi bisa menemukan materi Ramadhan/adzan.
[ ] Aplikasi bisa menemukan podcast/event/live source.
[ ] Aplikasi bisa membuat struktur folder fresh.
[ ] Aplikasi bisa copy file approved.
[ ] Aplikasi bisa generate playlist .m3u8.
[ ] Aplikasi bisa generate scheduler plan.
[ ] Aplikasi bisa generate fallback playlist.
[ ] Aplikasi bisa generate laporan CSV/JSON/HTML/MD.
[ ] Tidak ada file lama dihapus otomatis.
[ ] Semua aksi besar perlu approval.
[ ] Output siap dipakai admin untuk setup ulang RadioBOSS.
```

---

# Pembaruan Roadmap v2 Berdasarkan Screenshot

## Versi 0.1 Tambahan Wajib

Selain Full Drive Scanner, versi 0.1 harus mencakup:

- Scheduler Emergency Analyzer.
- Missing Path / Error Code 2 basic detector.
- Ramadhan/Adzan keyword detector.
- Report `scheduler_emergency_cleanup.csv`.

## Versi 0.2 Tambahan Wajib

- Scheduler Command Parser untuk `getfile`, `multiple`, `getrandomplaylist`, `load`, `play`, `stop`.
- Auto-Intro Asset Validator.
- Old Source Path Usage Report.

## Versi 0.3 Tambahan Wajib

- Cart Wall Rebuild Planner.
- Dirty Metadata Detector.
- Ramadhan Seasonal Archive Planner.

## Acceptance Criteria v2

Aplikasi belum boleh dianggap siap jika belum bisa:

- Menandai semua event Ramadhan/Sahur/Imsak/Hikmah Puasa sebagai seasonal archive.
- Menandai Jingle Ramadhan Rotasi sebagai seasonal, bukan jingle reguler.
- Menemukan missing path penyebab Error code 2.
- Menilai risiko `getrandomplaylist` dari folder mentah.
- Membuat rencana cart wall baru yang memisahkan STATION ID, JINGLE PROGRAM, SWEEPER, ILM/SPOT PUBLIK, LATAR, SPECIAL EVENT, RELIGI, RAMADHAN ONLY, dan EMERGENCY.
- Menandai metadata kotor seperti `PlanetLagu.com`.
