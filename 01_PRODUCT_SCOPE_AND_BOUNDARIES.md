# 01 — Product Scope and Boundaries

## Nama Kerja

```text
RadioBOSS Fresh Reset Manager
```

## Tujuan Aplikasi

Aplikasi desktop lokal untuk membantu admin/operator studio melakukan reset fresh RadioBOSS secara terstruktur:

- audit total aset RadioBOSS lama,
- temukan playlist dan file bermasalah,
- pisahkan aset siaran sesuai kategori,
- buat struktur folder baru,
- generate playlist `.m3u8`,
- siapkan scheduler plan,
- siapkan special event, podcast, live source, dan fallback.

## Yang Masuk Scope

### Audit dan Discovery

- Full drive scan.
- Scan folder pilihan.
- Deteksi playlist `.m3u`, `.m3u8`, `.pls`.
- Deteksi file audio: `.mp3`, `.wav`, `.flac`, `.m4a`, `.aac`, `.ogg`, `.wma`.
- Deteksi file dokumen pendukung kecil: `.txt`, `.csv`, `.json`, `.xml`, `.ini` jika relevan.
- Deteksi aset Ramadhan, adzan, imsak, takbiran, shalawat, jingle, sweeper, ILM, iklan, podcast, relay, event.

### Cleanup Preparation

- Backup inventory.
- Cleanup plan.
- Folder fresh builder.
- Copy approved files.
- Quarantine review.
- Archive recommendation.

### Playlist dan Scheduler

- Audit playlist lama.
- Deteksi missing path.
- Deteksi playlist dangerous.
- Generate playlist `.m3u8` baru.
- Generate scheduler plan `.csv` dan `.md`.
- Generate manifest.

### Program Khusus

- Liputan khusus.
- Special event.
- Podcast.
- Talkshow.
- Relay YouTube.
- External stream.
- WhatsApp call.
- Discord/Zoom/Google Meet.
- Lagu khusus.
- Emergency fallback.

## Yang Tidak Masuk Scope Tahap Ini

- Integrasi dengan Aplikasi Radio SBL.
- Sinkron Firestore atau jadwal penyiar Radio SBL.
- Absensi penyiar.
- Request lagu dari aplikasi Radio SBL.
- Naskah AI.
- Rename massal file musik mentah tanpa approval.
- Editing metadata massal tanpa preview.
- Menghapus file lama secara permanen.
- Menulis langsung ke konfigurasi internal RadioBOSS tanpa backup.

## Mode Operasi

### 1. Audit Only

Tidak mengubah file apa pun.

Output:

```text
- audit_summary.csv
- playlist_lama_report.csv
- dangerous_items.csv
```

### 2. Fresh Reset Maintenance

RadioBOSS diasumsikan sedang stop siaran. Aplikasi boleh melakukan deep scan, metadata read, copy file, generate struktur, dan export playlist.

Tetap tidak boleh hapus permanen.

### 3. Advanced Apply

Untuk versi lanjutan. Dapat mengirim command ke RadioBOSS atau menggunakan API/command line jika sudah aman. Jangan implementasikan di versi awal kecuali sebagai stub.

## Safety Rules

1. Semua aksi perubahan harus tercatat di `cleanup_plan.csv`.
2. Semua file hasil copy harus tercatat di `copy_manifest.csv`.
3. File lama tidak dihapus.
4. Struktur baru dibuat di root fresh, contoh `D:\RADIO_SBL_FRESH`.
5. Jika klasifikasi ragu, file masuk `REVIEW`, bukan aktif.
6. Semua materi musiman default diblok dari playlist reguler.
7. Semua adzan hanya boleh dipakai sebagai event khusus, bukan playlist acak.
8. Semua relay/live call harus punya fallback.
