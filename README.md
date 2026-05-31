# RadioBOSS Fresh Reset Manager 📻✨

Aplikasi desktop lokal berbasis web lokal (**Python Flask + SQLite + Premium HTML/CSS/JS**) yang dirancang khusus untuk membantu reset bersih (fresh reset), audit pustaka audio, pemilahan materi musiman (Ramadhan), perbaikan jalur berkas rusak (**Error Code 2**), dan penjadwalan siaran ulang secara steril, aman, dan profesional untuk **Radio SBL 92.4**.

---

## 🔍 1. Latar Belakang & Temuan Masalah Nyata

Aplikasi ini dibangun untuk mengatasi kendala siaran RadioBOSS yang berantakan berdasarkan analisis tangkapan layar nyata:
1. **Playback Terputus (Error Code 2)**: Log RadioBOSS sering menampilkan `Unable to play! Error code 2`, yang dipicu oleh berkas hilang, jalur (path) yang terputus ke drive lama stasiun, atau playlist yang rusak.
2. **Event Musiman Aktif**: Event scheduler reguler masih memuat grup dan rotasi **RAMADHAN 2026** (seperti Tips Sahur, Imsak, Hikmah Puasa, Berbuka Puasa, dan Jingle Ramadhan) di luar bulan suci.
3. **Cart Wall Panel Kanan Bercampur**: Item station ID, sweeper jingle, spot iklan komersial, Bed Music (instrumental latar), dan materi Ramadhan menumpuk dalam satu tab tidak teratur.
4. **Command Penjadwalan Berisiko Tinggi**: Adanya pemanggilan command `getrandomplaylist` dari folder mentah kotor (seperti `E:\agus lagu baru`) yang rawan memicu crash playback.
5. **Metadata Kotor Watermark Internet**: Banyak aset audio yang mengandung label watermark unduhan website pihak ketiga seperti `PlanetLagu.com`, `Stafaband`, dan sejenisnya.

---

## 🛠️ 2. Arsitektur & Teknologi

Untuk menghadirkan pengalaman pengguna stasiun radio yang responsif dan memukau, aplikasi ini mengadopsi stack modern:
- **Backend (Python Flask)**: Sangat andal untuk pemindaian filesystem Windows secara cepat, manipulasi data SQLite, penguraian teks playlist, dan otomasi copy.
- **Database Lokal (SQLite)**: Menyimpan indeks berkas secara persisten selama maintenance offline agar data instan dimuat di dashboard UI.
- **Frontend Premium (Vanilla HTML5, CSS Glassmorphism, JS Fetch API)**: Antarmuka modern dengan gaya **Dark Mode** beraksen warna neon pekat, micro-animation responsif pada tombol, dan status badge visual.
- **Launcher Windows (`run.bat`)**: Cukup dobel-klik skrip launcher ini untuk menginstal dependensi dan membuka browser secara otomatis ke alamat `http://localhost:5000/`.

---

## 🚀 3. Fitur Utama Aplikasi

1. **Full Drive/Folder Scanner**: Memindai filesystem secara rekursif, mengabaikan folder sistem (seperti `node_modules`, `.git`), dan mengindeks file audio (`.mp3`, `.wav`, dll.) serta playlist (`.m3u8`, `.pls`).
2. **Classifier & Danger Detector**: Memilah tipe berkas audio secara cerdas berdasarkan `keyword_rules.json` untuk menandai seasonal Ramadhan, adzan, spot ILM, jingle stasiun, sweeper, bed music latar, dan melabeli metadata kotor.
3. **Playlist Auditor**: Mengaudit file playlist lama stasiun radio, melacak missing path pemicu Error Code 2, dan menyusun saran perbaikan (relink).
4. **Scheduler Emergency Analyzer**: Mengurai grup event scheduler RadioBOSS yang tidak aktif/risiko tinggi (Ramadhan di luar musim, command random source mentah) dan merekomendasikan penonaktifannya.
5. **Cart Wall Rebuild Planner**: Menyusun pembagian tab cart wall baru yang steril (Tab Station ID, Jingle Program, Sweeper, ILM/Spot Publik, Latar/Bed Music).
6. **Fresh Folder Structure Builder**: Membangun struktur folder steril target `D:\RADIO_SBL_FRESH` yang bersih dari data kotor lama.
7. **Safe Copy Manager**: Menyalin berkas approved secara aman (Dry-Run + Aksi Fisik) ke folder steril stasiun radio tanpa mengubah atau menghapus data asli.
8. **Playlist & Scheduler Plan Builder**: Membuat 4 file playlist `.m3u8` steril yang baru (SALAM_SUBUH, SEMANGAT_PAGI, ILM_EDUKASI, RELIGI_REGULER) bebas dari materi Ramadhan, serta menyusun rencana event scheduler baru.
9. **Laporan & Dokumen Ekspor Terpadu**: Menghasilkan 14 laporan CSV detail dan dokumen Markdown panduan setup manual di folder steril dan output aplikasi.

---

## 📂 4. Struktur Proyek

```text
radioboss_fresh_reset_manager/
├── run.py                          # Skrip utama backend (Flask server)
├── run.bat                         # Startup launcher otomatis Windows
├── requirements.txt                # Dependensi Python (Flask, dll.)
├── README.md                       # Dokumentasi resmi ini
├── config/
│   ├── app_config.json             # Konfigurasi fresh root, default scan, dll.
│   └── keyword_rules.json          # Aturan kata kunci deteksi risiko audio
├── core/
│   ├── scanner.py                  # Pemindai filesystem rekursif
│   ├── classifier.py               # Pemilah kategori audio & deteksi bahaya
│   ├── playlist_parser.py          # Pengurai file playlist (.m3u, .pls)
│   ├── playlist_auditor.py         # Analisis missing paths pemicu Error 2
│   ├── scheduler_emergency_analyzer.py # Pemilah event scheduler & risiko
│   ├── cart_wall_planner.py        # Penata ulang cart wall stasiun radio
│   ├── fresh_folder_builder.py     # Pembuat struktur folder steril baru
│   ├── copy_manager.py             # Pengelola salinan file aman (Dry-Run)
│   ├── m3u8_generator.py           # Pembuat playlist .m3u8 reguler steril baru
│   ├── scheduler_plan_builder.py   # Pembuat rencana event scheduler baru
│   └── report_writer.py            # Pembuat laporan CSV, MD, & manifest
├── db/
│   ├── database.py                 # Wrapper SQLite database lokal
│   └── schema.sql                  # Struktur skema tabel database
├── ui/
│   ├── templates/                  # Template halaman dashboard HTML
│   │   └── index.html
│   └── static/                     # Aset styling CSS premium & JS Fetch
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
└── tests/                          # Skrip pengujian otomatis (unit tests)
    ├── test_playlist_parser.py
    └── test_classifier.py
```

---

## 🏃‍♂️ 5. Cara Menjalankan Aplikasi di Windows

1. Pastikan Anda telah menginstal **Python (versi 3.8 ke atas)** dan mencentang opsi **"Add Python to PATH"** saat instalasi.
2. Unduh/klon repositori stasiun radio ini ke disk lokal komputer Anda.
3. Dobel-klik berkas **`run.bat`** di direktori root aplikasi.
4. Skrip launcher akan secara otomatis memasang dependensi (Flask) ke sistem, meluncurkan server lokal Flask pada port `5000`, dan membuka browser default stasiun radio langsung ke alamat:
   👉 **`http://localhost:5000/`**

---

## 🔄 6. Urutan Alur Reset Steril (Fresh Reset Workflow)

Untuk melakukan penataan ulang yang steril dan aman, jalankan langkah-langkah di Web Dashboard sesuai nomor urutan aksi cepat:

1. **Langkah 1 (Pindai & Audit Pustaka)**:
   - Pilih direktori input (misal folder demo default `D:\RADIO_MUSIC_INPUT_DEMO`) di tab **Drive Scan**, lalu klik **Mulai Scan Pustaka**.
   - Sistem akan mengindeks file audio, memilah materi Ramadhan, menandai file kotor, mengaudit playlist lama yang rusak (Error Code 2), serta mendeteksi scheduler risiko tinggi.
2. **Langkah 2 (Bangun Struktur Folder)**:
   - Buka tab **Folder & Copier**, lalu klik **Bangun Struktur Direktori**.
   - Folder steril target akan dibangun secara otomatis di `D:\RADIO_SBL_FRESH\` lengkap dengan manifestnya.
3. **Langkah 3 (Salin Aset Approved)**:
   - Klik tombol **Mulai Salin Aset** di tab **Folder & Copier**.
   - Seluruh lagu stasiun radio yang bersih (`APPROVED`) akan disalin secara fisik ke folder kategori steril yang sesuai tanpa menyentuh file asli Anda. Konflik nama diselesaikan otomatis dengan short hash.
4. **Langkah 4 (Susun Playlist & Scheduler Plan Baru)**:
   - Klik **Susun Playlist & Plan** di dashboard utama stasiun radio.
   - Sistem akan menyusun 4 file playlist `.m3u8` steril pembawa siaran reguler (bebas materi Ramadhan/adzan) dan rencana scheduler siaran yang baru.
5. **Langkah 5 (Ekspor Laporan & Dokumen Panduan)**:
   - Buka tab **Reports & Logs**, klik **Ekspor Seluruh Laporan CSV/MD**.
   - Seluruh berkas laporan audit pustaka dan panduan langkah setup manual administrator akan diekspor ke folder `output/reports/` dan folder steril target.

---

## 📋 7. Panduan Setup Akhir Manual Administrator

Setelah menjalankan seluruh pipeline di Web Dashboard, administrator stasiun radio cukup melakukan setup manual di RadioBOSS fisik dengan panduan berkas:
📄 **`D:\RADIO_SBL_FRESH\09_LAPORAN_RESET\final_setup_checklist.md`**

Secara ringkas:
- **Langkah 1**: Backup konfigurasi lama RadioBOSS Anda ke folder `D:\RADIO_SBL_FRESH\00_ARSIP_LAMA\`.
- **Langkah 2**: Buka tab **Scheduler** RadioBOSS, nonaktifkan/hapus grup `RAMADHAN 2026` lama beserta event pendukung musiman lainnya.
- **Langkah 3**: Buka tab **Playlist** RadioBOSS, impor 4 file playlist `.m3u8` steril reguler baru dari folder `D:\RADIO_SBL_FRESH\07_PLAYLIST_BARU\`.
- **Langkah 4**: Di panel kanan (**Cart Wall**), buat tab baru sesuai rencana pada laporan `cart_wall_rebuild_plan.csv` dan tarik berkas audio jingle stasiun yang bersih ke slot masing-masing.
- **Langkah 5**: Tambahkan 5 event siaran baru secara manual sesuai detail rencana di `radioboss_scheduler_plan.csv`.

---

## 🧪 8. Menjalankan Pengujian Otomatis (Unit Tests)

Anda dapat memverifikasi kelayakan dan stabilitas seluruh logika modul backend Python secara offline kapan saja menggunakan perintah berikut pada PowerShell/CMD stasiun radio:

```bash
python -m unittest discover -s tests
```

Output pengujian yang sukses:
```text
Ran 5 tests in 0.020s

OK
```

---

## 🔒 9. Prinsip Keamanan Sistem

- **JANGAN UBAH BERKAS ASLI**: Aplikasi ini 100% menggunakan aksi menyalin (**COPY**), bukan memindahkan atau menghapus, untuk menjamin keselamatan penuh aset pustaka lama Anda.
- **JANGAN OVERWRITE TANPA PROTEKSI**: Konflik penamaan ditangani otomatis dengan membubuhkan hash MD5 unik demi menghindari tertimpanya berkas audio berbeda yang bernama sama.
- **OFFLINE MAINTENANCE**: Sistem 100% gratis dan berjalan lokal di PC studio Anda tanpa memanggil API berbayar online apa pun.
