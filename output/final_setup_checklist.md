# Panduan Setup Akhir Manual RadioBOSS (Final Setup Checklist)

Ikuti instruksi langkah-demi-langkah berikut untuk mengaktifkan kembali siaran stasiun radio Radio SBL secara steril dan aman:

### Langkah 1: Backup Konfigurasi RadioBOSS Lama
- [ ] Buka RadioBOSS, klik menu **Settings** -> **Backup/Restore** -> **Backup settings to file...**
- [ ] Simpan file backup dengan nama `RadioBOSS_Backup_Sebelum_Reset.zip` ke folder steril `D:\RADIO_SBL_FRESH\00_ARSIP_LAMA`.

### Langkah 2: Pembersihan Grup Scheduler Ramadhan Lama
- [ ] Buka tab **Scheduler** di panel kiri RadioBOSS.
- [ ] Nonaktifkan (uncheck) grup `RAMADHAN 2026`.
- [ ] Klik kanan event `berbuka puasa`, `Tips Sahur`, `Imsak`, `Hikmah Puasa`, lalu pilih **Disable** atau **Delete** dari regular scheduler.

### Langkah 3: Impor Playlist Baru Steril
- [ ] Tarik file-file playlist baru dari `D:\RADIO_SBL_FRESH\07_PLAYLIST_BARU\`:
  - `0500_SALAM_SUBUH.m3u8`
  - `0700_SEMANGAT_PAGI.m3u8`
  - `1300_ILM_EDUKASI.m3u8`
  - `1800_RELIGI_REGULER.m3u8`
- [ ] Pastikan tidak ada pesan error `Unable to play! Error code 2` saat pemutaran simulasi.

### Langkah 4: Pengaturan Ulang Cart Wall stasiun radio
- [ ] Di panel kanan (Cart Wall), klik kanan tab kosong untuk membuat tab baru:
  - Buat **Tab 1: STATION ID**
  - Buat **Tab 2: JINGLE PROGRAM**
  - Buat **Tab 3: SWEEPER**
  - Buat **Tab 4: ILM / SPOT PUBLIK**
  - Buat **Tab 5: LATAR / BED MUSIC**
- [ ] Tarik berkas audio jingle dan spot yang bersih ke masing-masing slot sesuai laporan `cart_wall_rebuild_plan.csv`.

### Langkah 5: Impor Rencana Event Scheduler Baru
- [ ] Buka jendela Scheduler RadioBOSS, klik tombol **Add** untuk menambahkan event baru secara manual sesuai rencana di `radioboss_scheduler_plan.csv`.
- [ ] Cek status playback adzan otomatis saat event Maghrib berbunyi.
- [ ] Selamat! Siaran stasiun radio Anda kini kembali segar, rapi, dan profesional.
