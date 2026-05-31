# 16 — Prompt Eksekusi Developer Berdasarkan Screenshot RadioBOSS

Gunakan prompt ini di Gemini/Codex setelah membaca semua dokumen sebelumnya.

## Prompt Utama

Anda adalah developer senior yang membangun aplikasi desktop Windows bernama **RadioBOSS Fresh Reset Manager** untuk membantu reset maintenance RadioBOSS milik Radio SBL 92.4.

Aplikasi ini bukan sekadar playlist generator. Berdasarkan screenshot RadioBOSS, kondisi nyata menunjukkan:

1. Scheduler masih berisi grup Ramadhan 2026, Subuh/Sahur, Imsak, Hikmah Puasa, Berbuka Puasa, dan Jingle Ramadhan.
2. Scheduler masih memanggil command `getfile`, `multiple`, dan `getrandomplaylist` dari folder lama seperti `E:\agus lagu baru` dan `E:\SUARA BUMI LASINRANG 2025`.
3. Playlist aktif menampilkan banyak lagu dari folder/metadata kotor, termasuk sumber download seperti PlanetLagu.com.
4. Log RadioBOSS menampilkan `Unable to play! Error code 2`, sehingga aplikasi wajib mendeteksi path missing, invalid file, dan target playlist rusak.
5. Cart wall/tab kanan bercampur antara Spot, Jingle, Latar, ILM, Instrumental, Ramadhan, dan program jingle.
6. Jingle Ramadhan masih tampil di area aktif dan harus dipisahkan ke seasonal archive.
7. Adzan harus divalidasi sebagai event khusus, bukan masuk playlist acak.

Bangun aplikasi secara bertahap dengan fokus maintenance offline karena RadioBOSS akan dihentikan selama proses reset.

## Modul yang wajib dibuat

1. Full Drive Scanner.
2. Playlist Auditor.
3. Scheduler Emergency Analyzer.
4. Scheduler Command Parser.
5. Danger Detector untuk Ramadhan/Adzan/Seasonal.
6. Missing Path & Error Code 2 Resolver.
7. Auto-Intro Asset Validator.
8. Cart Wall Rebuild Planner.
9. Fresh Folder Structure Builder.
10. Playlist Rebuilder M3U8.
11. Clock & Scheduler Plan Generator.
12. Live Source & Event Planner.
13. Emergency Fallback Builder.
14. Report Writer.
15. Before/After Reset Summary.

## Larangan implementasi

Jangan membuat fitur yang:

- menghapus file lama permanen,
- overwrite konfigurasi RadioBOSS tanpa backup,
- menonaktifkan scheduler langsung tanpa preview,
- move file asli sebagai default,
- mengubah metadata massal tanpa review,
- menganggap semua file religi sebagai Ramadhan,
- menganggap semua jingle sebagai jingle reguler,
- memasukkan podcast/liputan khusus ke playlist musik reguler.

Default action adalah **copy**, bukan move. Default workflow adalah **scan → audit → preview → approve → build fresh → export → manual apply → test**.

## Output minimal versi pertama

Aplikasi versi awal wajib menghasilkan file berikut:

```text
reports/drive_scan_summary.csv
reports/playlist_audit.csv
reports/scheduler_emergency_cleanup.csv
reports/scheduler_command_risk.csv
reports/missing_paths_report.csv
reports/auto_intro_validation.csv
reports/cart_wall_rebuild_plan.csv
reports/ramadhan_adzan_report.csv
reports/dirty_metadata_report.csv
reports/old_source_path_usage.csv
reports/before_after_reset_summary.md
output/playlists/0500_SALAM_SUBUH.m3u8
output/playlists/0700_SEMANGAT_PAGI.m3u8
output/playlists/1300_ILM_EDUKASI.m3u8
output/playlists/1800_RELIGI_REGULER.m3u8
output/scheduler_plan/radioboss_scheduler_plan.csv
output/final_setup_checklist.md
```

## Acceptance test berbasis kondisi screenshot

Aplikasi dinyatakan lolos jika mampu:

1. Menemukan event `RAMADHAN 2026` dan menandainya sebagai `SEASONAL_RAMADHAN_ARCHIVE`.
2. Menemukan event `Tips Sahur`, `Imsak`, `Hikmah Puasa`, dan `berbuka puasa.m3u8` sebagai seasonal.
3. Menemukan `JINGLE RAMADHAN ROTASI.m3u8` sebagai seasonal dan bukan jingle reguler.
4. Menemukan event adzan dan menandainya sebagai `ADZAN_REVIEW`.
5. Menemukan command `getrandomplaylist` dari folder mentah dan menandainya sebagai `DANGEROUS_RANDOM_SOURCE`.
6. Menemukan playlist yang memuat path hilang/invalid dan membuat laporan missing path.
7. Menemukan item cart wall seperti ILM/Stop Bullying/Jauhi Narkoba dan memindahkannya ke rencana tab ILM/SPOT PUBLIK.
8. Menemukan instrumental saxophone dan memindahkannya ke rencana tab LATAR/BED MUSIC.
9. Menemukan jingle program seperti Salam Subuh, Aga Kareba, SBL on Stage sebagai JINGLE_PROGRAM.
10. Menemukan keyword `PlanetLagu.com` dan menandainya sebagai dirty metadata.

## Output UX wajib

Buat UI desktop sederhana dengan tab:

```text
Dashboard
Drive Scan
Playlist Audit
Scheduler Audit
Error Code 2 / Missing Path
Cart Wall Planner
Ramadhan & Adzan
Clock Builder
Live Source & Event
Emergency Fallback
Reports
Settings
```

Dashboard harus menampilkan angka kritis:

- Playlist ditemukan.
- Playlist rusak.
- Missing path.
- Event Ramadhan aktif/terdeteksi.
- Event adzan perlu review.
- Source path lama.
- Cart wall item perlu dipindah.
- Dirty metadata.
- Status siap reset.

## Prinsip final

Jangan menambal RadioBOSS lama. Bangun workflow fresh reset:

```text
backup → full scan → audit → klasifikasi → seasonal archive → fresh structure → rebuild playlist → scheduler plan → test → on-air
```
