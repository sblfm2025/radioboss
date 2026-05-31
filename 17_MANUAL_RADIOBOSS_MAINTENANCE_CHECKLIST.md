# 17 — Checklist Manual Maintenance RadioBOSS Setelah Aplikasi Selesai Generate

Dokumen ini dipakai operator/admin setelah aplikasi RadioBOSS Fresh Reset Manager selesai membuat laporan dan file export. Tujuannya memastikan RadioBOSS kembali on-air dalam kondisi fresh dan tidak membawa masalah lama.

## 1. Sebelum Membuka RadioBOSS Kembali

- [ ] Semua laporan aplikasi sudah dibuat.
- [ ] Folder fresh sudah terbentuk.
- [ ] Playlist baru sudah dihasilkan.
- [ ] Scheduler plan baru sudah dihasilkan.
- [ ] `before_after_reset_summary.md` sudah dibaca.
- [ ] Tidak ada warning CRITICAL yang belum ditangani.
- [ ] Semua file lama masih aman di backup/arsip.

## 2. Disable Scheduler Lama

Di RadioBOSS:

- [ ] Buka Scheduler.
- [ ] Backup/screenshot semua event lama.
- [ ] Disable semua grup/event Ramadhan 2026.
- [ ] Disable semua Tips Sahur.
- [ ] Disable semua Imsak.
- [ ] Disable semua Hikmah Puasa.
- [ ] Disable semua Berbuka Puasa.
- [ ] Disable semua Jingle Ramadhan Rotasi.
- [ ] Disable semua playlist operator lama yang tidak jelas.
- [ ] Review event adzan satu per satu.

Jangan hapus dulu sebelum sistem baru stabil minimal 1–2 minggu.

## 3. Bersihkan Cart Wall

- [ ] Jangan gunakan tab JINGLE lama sebagai rujukan akhir.
- [ ] Pindahkan SP4N LAPOR, Stop Bullying, Jauhi Narkoba, Bahaya Judol, dan sejenisnya ke tab ILM/SPOT PUBLIK.
- [ ] Pindahkan instrumental ke tab LATAR/BED MUSIC.
- [ ] Pindahkan Salam Subuh, Aga Kareba, SBL on Stage, Informasi Seputar Pinrang ke tab JINGLE PROGRAM.
- [ ] Pindahkan Jingle Ramadhan dan OASE Ramadhan ke RAMADHAN ONLY.
- [ ] Siapkan tab EMERGENCY.

## 4. Arahkan RadioBOSS ke Folder Fresh

- [ ] Pastikan RadioBOSS tidak lagi mengambil dari folder `E:\agus lagu baru` sebagai sumber acak.
- [ ] Pastikan RadioBOSS tidak lagi mengambil dari folder Ramadhan lama.
- [ ] Pastikan playlist aktif berasal dari folder fresh.
- [ ] Pastikan jingle/spot aktif berasal dari folder fresh.
- [ ] Pastikan ILM aktif berasal dari folder fresh.
- [ ] Pastikan adzan berasal dari folder adzan khusus.

## 5. Load Playlist Baru

Uji playlist berikut:

- [ ] 0500_SALAM_SUBUH.m3u8
- [ ] 0700_SEMANGAT_PAGI.m3u8
- [ ] 0800_PROGRAM_PAGI.m3u8
- [ ] 1300_ILM_EDUKASI.m3u8
- [ ] 1800_RELIGI_REGULER.m3u8
- [ ] 2000_PROGRAM_MALAM.m3u8
- [ ] 2200_LAGU_TERBAIK.m3u8
- [ ] EMERGENCY_GENERAL.m3u8

Untuk setiap playlist:

- [ ] Tidak ada file missing.
- [ ] Tidak ada Ramadhan-only.
- [ ] Tidak ada adzan di playlist acak.
- [ ] Tidak ada file review.
- [ ] Tidak ada iklan expired.
- [ ] Tidak ada podcast/liputan khusus kecuali pada clock khusus.

## 6. Setup Scheduler Baru

Buat event minimal:

```text
05:00 CLOCK_SALAM_SUBUH
07:00 CLOCK_SEMANGAT_PAGI
08:00 CLOCK_PROGRAM_PAGI
10:00 CLOCK_LASINRANG_PRENEUR
11:30 CLOCK_KELUARGA_BERDAYA
13:00 CLOCK_ILM_EDUKASI
14:00 CLOCK_INFO_PINRANG
16:00 CLOCK_PROGRAM_SORE
18:00 CLOCK_RELIGI_REGULER
20:00 CLOCK_PROGRAM_MALAM
22:00 CLOCK_LAGU_TERBAIK
23:00 CLOCK_NIGHT_SAFE
```

Adzan dibuat terpisah:

```text
ADZAN_SUBUH
ADZAN_DZUHUR
ADZAN_ASHAR
ADZAN_MAGHRIB
ADZAN_ISYA
```

Ramadhan dibuat tapi nonaktif di luar musim:

```text
RAMADHAN_IMSAK_NONAKTIF
RAMADHAN_SAHUR_NONAKTIF
RAMADHAN_BUKA_PUASA_NONAKTIF
RAMADHAN_JINGLE_NONAKTIF
```

## 7. Test Playback

- [ ] Play 10 item pertama setiap playlist.
- [ ] Skip beberapa item untuk melihat error.
- [ ] Pastikan tidak ada Error code 2.
- [ ] Pastikan auto-intro file valid.
- [ ] Pastikan volume jingle tidak terlalu besar/kecil.
- [ ] Pastikan silence detector tetap aktif.
- [ ] Pastikan scheduler aktif hanya setelah event baru benar.

## 8. Test Event Khusus

- [ ] Test playlist Podcast.
- [ ] Test playlist Liputan Khusus.
- [ ] Test playlist Special Event.
- [ ] Test fallback YouTube relay.
- [ ] Test fallback live call.
- [ ] Test emergency playlist.

## 9. Final On-Air Approval

RadioBOSS boleh kembali on-air jika:

- [ ] Tidak ada warning CRITICAL.
- [ ] Playlist reguler bersih.
- [ ] Scheduler lama sudah disabled.
- [ ] Event Ramadhan tidak aktif.
- [ ] Adzan sudah benar.
- [ ] Cart wall sudah dipisah.
- [ ] Emergency fallback tersedia.
- [ ] Operator memahami struktur baru.

## 10. Monitoring 7 Hari Pertama

Selama 7 hari pertama:

- [ ] Catat semua error playback.
- [ ] Catat lagu yang salah kategori.
- [ ] Catat jingle/ILM yang salah tempat.
- [ ] Catat event scheduler yang tidak sesuai.
- [ ] Jangan mengaktifkan kembali playlist lama tanpa review.
- [ ] Jangan menambahkan file baru langsung ke folder aktif; masukkan ke REVIEW dulu.
