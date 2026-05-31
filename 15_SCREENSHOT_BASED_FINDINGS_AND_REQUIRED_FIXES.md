# 15 — Temuan Screenshot RadioBOSS & Perbaikan Wajib

Dokumen ini adalah pembaruan penting berdasarkan tangkapan layar RadioBOSS terbaru. Developer wajib menjadikan temuan ini sebagai dasar prioritas implementasi, karena masalah yang terlihat bukan hanya playlist berantakan, tetapi campuran antara scheduler lama, cart wall, Ramadhan, adzan, auto-intro, missing path, metadata kotor, dan folder sumber yang tersebar.

## 1. Ringkasan Kondisi Nyata dari Screenshot

Temuan utama:

1. Playlist utama masih memakai library campur dan metadata kotor.
2. Log RadioBOSS menampilkan `Unable to play! Error code 2`, artinya ada file hilang, path invalid, file rusak, atau format tidak bisa dibuka.
3. Auto-intro masih menyisipkan file seperti `spot sbl short` dari path lama.
4. Scheduler masih memuat event Ramadhan, Sahur, Imsak, Hikmah Puasa, Berbuka Puasa, dan Jingle Ramadhan.
5. Scheduler adzan aktif, tetapi harus divalidasi jam dan path targetnya.
6. Cart wall/tab kanan bercampur antara Jingle, Spot, ILM, Latar, Ramadhan, dan Instrumental.
7. Ada folder sumber berisiko seperti `E:\agus lagu baru`, `E:\SUARA BUMI LASINRANG 2025`, dan folder lama lain yang langsung dipakai RadioBOSS.
8. Ada item yang mengandung watermark/sumber download seperti `PlanetLagu.com`.

Kesimpulan: aplikasi harus dibuat sebagai **Fresh Reset Maintenance Tool**, bukan hanya playlist generator.

## 2. Prioritas Perbaikan Berdasarkan Screenshot

Urutan prioritas wajib:

1. Scheduler Emergency Cleanup.
2. Missing Path & Error Code 2 Resolver.
3. Auto-Intro Asset Validator.
4. Cart Wall Rebuild Planner.
5. Ramadhan/Seasonal Archive Enforcement.
6. Adzan Event Validator.
7. `getfile`, `multiple`, dan `getrandomplaylist` Command Parser.
8. Dirty Metadata/Source Download Detector.
9. Fresh Master Library Enforcement.
10. Before/After Reset Report.

## 3. Scheduler Emergency Cleanup

Developer wajib membuat modul `SchedulerEmergencyAnalyzer`.

Modul ini harus membaca/menerima data scheduler dari RadioBOSS, minimal melalui input manual/export/screenshot transcription jika format scheduler tidak bisa dibaca langsung.

### Kategori event yang wajib dideteksi

- RAMADHAN 2026
- berbuka puasa
- tips sahur
- imsak
- hikmah puasa
- jingle ramadhan
- kultum ramadhan
- shalawat ramadhan
- kumpulan lagu religi 2026
- adzan subuh/dzuhur/ashar/maghrib/isya
- getrandomplaylist dari folder mentah
- playlist operator lama

### Status rekomendasi event

Gunakan status berikut:

```text
KEEP_ACTIVE
DISABLE_NOW
SEASONAL_RAMADHAN_ARCHIVE
ADZAN_REVIEW
BROKEN_PATH
UNKNOWN_REVIEW
DANGEROUS_RANDOM_SOURCE
```

### Aturan klasifikasi

```text
Jika nama/event/target mengandung ramadhan, imsak, sahur, berbuka, tarawih, takbiran, hikmah puasa, kultum ramadhan:
  status = SEASONAL_RAMADHAN_ARCHIVE
  recommendedAction = Disable outside Ramadhan

Jika event memanggil JINGLE RAMADHAN ROTASI:
  status = SEASONAL_RAMADHAN_ARCHIVE
  recommendedAction = Remove from regular scheduler/cart wall

Jika event memanggil adzan:
  status = ADZAN_REVIEW
  recommendedAction = Validate time, target file, and local prayer schedule

Jika event memakai getrandomplaylist dari folder yang namanya mengandung lagu baru, campur, download, backup, lama:
  status = DANGEROUS_RANDOM_SOURCE
  recommendedAction = Replace source with clean master category
```

### Output wajib

`reports/scheduler_emergency_cleanup.csv`

Kolom:

```csv
event_group,event_name,time,command_type,target_path,target_exists,risk_level,status,recommended_action,notes
```

Contoh:

```csv
RAMADHAN 2026,berbuka puasa,18:14:40,load,E:\SUARA BUMI LASINRANG\berbuka puasa.m3u8,true,CRITICAL,SEASONAL_RAMADHAN_ARCHIVE,Disable outside Ramadhan
SUBUH,Imsak 04:42,04:42:00,multiple,E:\SUARA BUMI LASINRANG\RAMADHAN,true,CRITICAL,SEASONAL_RAMADHAN_ARCHIVE,Seasonal only
JINGLE,Jingle 1,03:00:00,load,JINGLE RAMADHAN ROTASI.m3u8,true,HIGH,SEASONAL_RAMADHAN_ARCHIVE,Remove from regular cart/scheduler
Pagi,indo pagi,07:00:00,getrandomplaylist,E:\agus lagu baru,true,HIGH,DANGEROUS_RANDOM_SOURCE,Do not use raw folder as random source
ADZAN,ADZAN MAGHRIB,18:08:00,play,E:\SUARA BUMI LASINRANG\Adzan - Radio SBL.mp3,true,MEDIUM,ADZAN_REVIEW,Verify local prayer time
```

## 4. Missing Path & Error Code 2 Resolver

Screenshot menunjukkan pesan `Unable to play! Error code 2`. Developer wajib membuat modul `PlaybackErrorResolver`.

### Fungsi modul

1. Scan semua playlist `.m3u`, `.m3u8`, `.pls`.
2. Baca semua path item playlist.
3. Cek apakah file target ada.
4. Cek apakah file berukuran 0 byte.
5. Cek ekstensi didukung.
6. Tandai path ke drive/folder lama.
7. Buat rekomendasi pengganti jika ada file serupa di master library.

### Status item

```text
OK
MISSING_FILE
ZERO_BYTE
UNSUPPORTED_EXTENSION
OLD_SOURCE_PATH
DUPLICATE_CANDIDATE
NEEDS_RELINK
```

### Output wajib

```text
reports/missing_paths_report.csv
reports/invalid_playlist_items.csv
reports/relink_candidates.csv
```

Kolom minimal:

```csv
playlist_file,item_path,status,file_exists,size_bytes,extension,recommended_relink,notes
```

## 5. Auto-Intro Asset Validator

Log menunjukkan auto-intro menyisipkan `spot sbl short` dan file jingle tertentu. Developer wajib membuat modul `AutoIntroValidator`.

### Fungsi

- Temukan semua referensi auto-intro/jingle yang dipakai RadioBOSS.
- Validasi file ada.
- Validasi durasi masuk akal.
- Validasi bukan file Ramadhan jika mode reguler.
- Validasi tidak berasal dari folder lama.
- Buat daftar file auto-intro yang harus dipindahkan ke struktur baru.

### Output

`reports/auto_intro_validation.csv`

Kolom:

```csv
auto_intro_name,target_path,exists,duration_seconds,is_ramadhan,is_old_path,status,recommended_action
```

## 6. Cart Wall Rebuild Planner

Screenshot menunjukkan tab `SPOT`, `LATAR`, dan `JINGLE` bercampur. Developer wajib membuat modul `CartWallPlanner`.

### Struktur cart wall baru

```text
TAB 1: STATION ID
TAB 2: JINGLE PROGRAM
TAB 3: SWEEPER
TAB 4: ILM / SPOT PUBLIK
TAB 5: LATAR / BED MUSIC
TAB 6: SPECIAL EVENT
TAB 7: RELIGI REGULER
TAB 8: RAMADHAN ONLY — nonaktif di luar Ramadhan
TAB 9: EMERGENCY
```

### Aturan pemindahan

- Item seperti `SP4N LAPOR`, `Jauhi Narkoba`, `Stop Kekerasan Terhadap Anak`, `Stop Bullying`, `Stop Judi Online`, `Bahaya Judol` = ILM/SPOT PUBLIK.
- Item `INSTRUMENTAL SAXOPHONE...` = LATAR/BED MUSIC.
- Item `Jingle SBL Ramadhan`, `Jingle OASE Ramadhan` = RAMADHAN ONLY.
- Item `Aga Kareba`, `SBL on Stage`, `Salam Subuh`, `Informasi Seputar Pinrang` = JINGLE PROGRAM.
- Item `Radio SBL - SBL Night Song`, `SBL Morning Song`, `SBL Multi Genre` = STATION ID / PROGRAM ID, tergantung durasi dan fungsi.

### Output

`reports/cart_wall_rebuild_plan.csv`

Kolom:

```csv
current_tab,slot,label,duration_seconds,current_path,detected_type,new_tab,new_folder,status,notes
```

## 7. Ramadhan/Seasonal Archive Enforcement

Semua materi Ramadhan harus dipindahkan ke struktur seasonal dan tidak boleh tampil di mode reguler.

### Folder target

```text
RADIO_SBL_FRESH/05_ADZAN_DAN_MUSIMAN/RAMADHAN_ONLY/
├── IMSAK/
├── SAHUR/
├── BUKA_PUASA/
├── HIKMAH_PUASA/
├── KULTUM_RAMADHAN/
├── SHALAWAT_RAMADHAN/
└── JINGLE_RAMADHAN/
```

### Rule blocking

```text
Jika asset.tag contains RAMADHAN_ONLY dan activeSeason != RAMADHAN:
  blockFromRegular = true
  blockFromCartWallRegular = true
  blockFromSchedulerRegular = true
```

## 8. Adzan Event Validator

Adzan harus tetap menjadi event khusus, bukan playlist acak.

### Validasi wajib

- File target ada.
- Event tidak memanggil playlist campur.
- Event tidak berada di folder Ramadhan.
- Jam adzan bisa direview manual.
- Nama event jelas.

### Output

`reports/adzan_event_validation.csv`

Kolom:

```csv
prayer,event_name,time,target_path,exists,status,recommended_action
```

## 9. Scheduler Command Parser

Developer wajib membuat parser minimal untuk command berikut:

```text
getfile
multiple
getrandomplaylist
load
play
stop
run
```

Tujuannya bukan menjalankan command, tetapi membaca risiko target.

### Risiko tinggi

- `getrandomplaylist` dari folder `lagu baru`.
- `multiple` dari folder campur.
- `load` playlist Ramadhan.
- `play` file yang tidak ada.
- `getfile` dari folder seasonal di luar musim.

### Output

`reports/scheduler_command_risk.csv`

## 10. Dirty Metadata & Source Download Detector

Screenshot menunjukkan item seperti `PlanetLagu.com`. Developer wajib menandai sumber download/metadata kotor.

### Keyword awal

```text
PlanetLagu
Stafaband
Gudang Lagu
Download Lagu
MP3 Juice
TikTok Version
Official Music Video
YouTube
[www.]
```

### Output

`reports/dirty_metadata_report.csv`

Kolom:

```csv
file_path,title,artist,album,comment,dirty_keyword,status,recommended_action
```

Status:

```text
DIRTY_METADATA
DIRTY_FILENAME
NEEDS_TAG_CLEANUP
OK
```

## 11. Fresh Master Library Enforcement

Setelah reset, RadioBOSS tidak boleh membaca langsung dari folder lama seperti:

```text
E:\agus lagu baru
E:\download
E:\lagu campur
E:\backup
E:\SUARA BUMI LASINRANG 2025\RAMADHAN
```

Semua sumber aktif harus diarahkan ke:

```text
E:\RADIO_SBL_FRESH\
```

atau path master yang dipilih user.

Aplikasi wajib membuat laporan:

`reports/old_source_path_usage.csv`

Kolom:

```csv
source_type,reference_file,old_path,risk,recommended_new_root,status
```

## 12. Before/After Reset Report

Aplikasi wajib menghasilkan ringkasan sebelum dan sesudah.

### Before

- Jumlah playlist lama.
- Jumlah playlist rusak.
- Jumlah path missing.
- Jumlah scheduler Ramadhan.
- Jumlah adzan event.
- Jumlah cart wall item bercampur.
- Jumlah file dirty metadata.
- Jumlah old source path.

### After

- Jumlah playlist aktif baru.
- Jumlah scheduler reguler baru.
- Jumlah seasonal item diarsipkan.
- Jumlah path invalid tersisa.
- Jumlah warning kritis tersisa.
- Status siap on-air.

Output:

```text
reports/before_after_reset_summary.md
reports/before_after_reset_summary.csv
```

## 13. Acceptance Criteria Tambahan

Fitur dianggap selesai jika:

- Aplikasi bisa menandai semua event Ramadhan/Sahur/Imsak/Jingle Ramadhan sebagai seasonal archive.
- Aplikasi bisa menemukan playlist yang mengandung path hilang.
- Aplikasi bisa membaca dan menilai risiko `getrandomplaylist`.
- Aplikasi bisa membuat rencana cart wall baru.
- Aplikasi bisa memblokir `RAMADHAN_ONLY` dari playlist reguler.
- Aplikasi bisa membuat laporan auto-intro yang file-nya hilang/tidak valid.
- Aplikasi bisa menandai metadata kotor seperti `PlanetLagu.com`.
- Aplikasi bisa membuat fresh master folder dan rencana perpindahan/copy.
- Aplikasi tidak menghapus file lama secara permanen.
- Aplikasi menghasilkan checklist final sebelum RadioBOSS on-air kembali.
