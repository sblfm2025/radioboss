# RadioBOSS Fresh Reset Manager — Overview Developer Pack

## Tujuan
Membangun aplikasi desktop lokal untuk membantu reset, audit, restrukturisasi, dan otomasi dasar RadioBOSS agar kembali rapi, fresh, profesional, dan mudah dioperasikan.

Aplikasi ini **bukan** aplikasi perapian file musik mentah dan **bukan** integrasi Aplikasi Radio SBL. Fokus aplikasi ini hanya pada:

1. Scan drive/folder terkait RadioBOSS.
2. Audit playlist lama RadioBOSS.
3. Audit aset siaran yang tersebar.
4. Deteksi risiko: Ramadhan-only, adzan, shalawat, imsak, takbiran, ILM/iklan kadaluarsa, playlist rusak.
5. Membuat struktur folder fresh.
6. Membuat playlist baru `.m3u8`.
7. Membuat clock siaran dan scheduler plan.
8. Menyiapkan workflow live source: YouTube relay, WhatsApp call, Discord, Zoom, podcast, special event, lagu khusus.
9. Membuat laporan before/after dan checklist final setup RadioBOSS.

## Prinsip Utama

- RadioBOSS dihentikan sementara saat reset, sehingga aplikasi boleh melakukan deep scan dan audit penuh.
- Tetap jangan melakukan aksi destruktif tanpa backup dan approval.
- Default aksi file adalah **COPY**, bukan MOVE.
- Jangan hapus file lama permanen.
- Jangan overwrite konfigurasi RadioBOSS tanpa backup.
- Semua hasil perubahan harus dapat diaudit melalui manifest dan laporan.

## Target Output Akhir

Setelah aplikasi dijalankan, tersedia folder fresh:

```text
D:\RADIO_SBL_FRESH\
├── 00_ARSIP_LAMA\
├── 01_MUSIC_ACTIVE\
├── 02_JINGLE_SWEEPER_ID\
├── 03_ILM\
├── 04_IKLAN\
├── 05_ADZAN_DAN_MUSIMAN\
├── 06_PROGRAM_ACARA\
├── 07_PLAYLIST_BARU\
├── 08_RADIOBOSS_EXPORT\
└── 09_LAPORAN_RESET\
```

Dan tersedia file:

```text
- audit_summary.csv
- dangerous_items.csv
- ramadhan_adzan_report.csv
- playlist_lama_report.csv
- missing_path_report.csv
- cleanup_plan.csv
- scheduler_plan.csv
- manifest.json
- final_setup_checklist.md
```

## Urutan Eksekusi Aplikasi

```text
1. Pilih mode Fresh Reset Maintenance.
2. Pilih drive/folder yang akan discan.
3. Jalankan full scan.
4. Audit playlist/audio/event khusus.
5. Review hasil klasifikasi.
6. Build struktur folder fresh.
7. Copy file approved ke struktur baru.
8. Generate playlist baru .m3u8.
9. Generate scheduler plan.
10. Generate checklist setup RadioBOSS.
11. Admin apply manual di RadioBOSS.
12. Test playback dan validasi final.
```

## Dokumen dalam Paket Ini

```text
00_README_OVERVIEW.md
01_PRODUCT_SCOPE_AND_BOUNDARIES.md
02_APP_ARCHITECTURE.md
03_FULL_DRIVE_SCANNER.md
04_CLASSIFICATION_AND_DANGER_DETECTION.md
05_FRESH_FOLDER_STRUCTURE.md
06_PLAYLIST_AUDIT_AND_REBUILD.md
07_CLOCK_AND_SCHEDULER_PLAN.md
08_SPECIAL_PROGRAMS_PODCAST_EVENTS.md
09_LIVE_SOURCE_AND_CALL_WORKFLOW.md
10_EMERGENCY_FALLBACK.md
11_DATABASE_AND_REPORTING.md
12_UI_UX_REQUIREMENTS.md
13_ROADMAP_AND_ACCEPTANCE_CHECKLIST.md
14_DEVELOPER_PROMPT_GEMINI_CODEX.md
```

---

## Pembaruan v2 Berdasarkan Screenshot RadioBOSS

Paket ini diperbarui berdasarkan tangkapan layar RadioBOSS yang menunjukkan kondisi nyata berikut:

- Log menampilkan `Unable to play! Error code 2`.
- Scheduler masih berisi grup `RAMADHAN 2026`, `SUBUH`, `JINGLE`, dan event seperti Tips Sahur, Imsak, Hikmah Puasa, Berbuka Puasa, serta Jingle Ramadhan Rotasi.
- Cart wall/tab kanan bercampur antara Jingle, Spot/ILM, Latar, Instrumental, dan Ramadhan.
- Ada command scheduler seperti `getfile`, `multiple`, dan `getrandomplaylist` dari folder sumber lama/mentah.
- Ada metadata/file kotor seperti `PlanetLagu.com`.

Dokumen tambahan v2:

```text
15_SCREENSHOT_BASED_FINDINGS_AND_REQUIRED_FIXES.md
16_RADIOBOSS_SCREENSHOT_CLEANUP_PROMPT.md
17_MANUAL_RADIOBOSS_MAINTENANCE_CHECKLIST.md
```

Developer wajib membaca dokumen 15 terlebih dahulu sebelum implementasi modul, karena dokumen tersebut mengunci prioritas teknis berdasarkan kondisi nyata RadioBOSS saat ini.
