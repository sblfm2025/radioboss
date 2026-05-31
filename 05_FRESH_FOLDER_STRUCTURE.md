# 05 — Fresh Folder Structure

## Tujuan

Membuat struktur folder baru yang bersih dan profesional untuk RadioBOSS.

## Root Folder

Default:

```text
D:\RADIO_SBL_FRESH\
```

Admin harus bisa mengubah root folder melalui Settings.

## Struktur Utama

```text
D:\RADIO_SBL_FRESH\
├── 00_ARSIP_LAMA\
│   ├── PLAYLIST_LAMA\
│   ├── SCHEDULER_LAMA\
│   ├── RAMADHAN_LAMA\
│   ├── CONFIG_BACKUP\
│   └── LAPORAN_AUDIT\
│
├── 01_MUSIC_ACTIVE\
│   ├── A_POWER_CURRENT_HIT\
│   ├── B_HOT_ROTATION\
│   ├── C_MEDIUM_ROTATION\
│   ├── D_GOLD_RECURRENT\
│   ├── E_NOSTALGIA\
│   ├── F_DANGDUT\
│   ├── G_RELIGI_REGULER\
│   └── H_LAGU_DAERAH_LOKAL\
│
├── 02_JINGLE_SWEEPER_ID\
│   ├── TOP_OF_HOUR\
│   ├── REGULAR_JINGLE\
│   ├── SWEEPER_PENDEK\
│   ├── BUMPER_PROGRAM\
│   ├── PROMO_PROGRAM\
│   └── TRANSISI\
│
├── 03_ILM\
│   ├── AKTIF\
│   ├── MUSIMAN\
│   ├── REVIEW\
│   └── KADALUARSA\
│
├── 04_IKLAN\
│   ├── AKTIF\
│   ├── SELESAI\
│   ├── REVIEW\
│   └── MATERI_MENTAH\
│
├── 05_ADZAN_DAN_MUSIMAN\
│   ├── ADZAN\
│   │   ├── SUBUH\
│   │   ├── DZUHUR\
│   │   ├── ASHAR\
│   │   ├── MAGHRIB\
│   │   └── ISYA\
│   ├── RAMADHAN_ONLY\
│   │   ├── IMSAK\
│   │   ├── SAHUR\
│   │   ├── BUKA_PUASA\
│   │   ├── TARAWIH\
│   │   ├── KULTUM_RAMADHAN\
│   │   └── SHALAWAT_RAMADHAN\
│   ├── IDUL_FITRI_ONLY\
│   └── IDUL_ADHA_ONLY\
│
├── 06_PROGRAM_ACARA\
│   ├── REGULER\
│   ├── LIPUTAN_KHUSUS\
│   ├── SPECIAL_EVENT\
│   ├── PODCAST\
│   ├── TALKSHOW\
│   ├── RELAY\
│   ├── LIVE_CALL\
│   ├── YOUTUBE_RELAY\
│   ├── ZOOM_DISCORD_MEETING\
│   └── CADANGAN_PROGRAM\
│
├── 07_PLAYLIST_BARU\
│   ├── REGULER_HARIAN\
│   ├── JAM_PER_JAM\
│   ├── LIPUTAN_KHUSUS\
│   ├── SPECIAL_EVENT\
│   ├── PODCAST\
│   ├── TALKSHOW\
│   ├── RELAY\
│   └── EMERGENCY\
│
├── 08_RADIOBOSS_EXPORT\
│   ├── M3U8\
│   ├── CLOCK\
│   ├── SCHEDULER_PLAN\
│   ├── LIVE_SOURCE_PLAN\
│   └── EMERGENCY_FALLBACK\
│
├── 09_REVIEW_KARANTINA\
│   ├── UNKNOWN\
│   ├── DUPLICATE_CANDIDATES\
│   ├── BROKEN_FILES\
│   └── NEEDS_MANUAL_CHECK\
│
└── 10_LAPORAN_RESET\
    ├── CSV\
    ├── JSON\
    ├── HTML\
    └── CHECKLIST\
```

## Builder Requirements

Fitur `Build Fresh Structure` harus:

1. Membuat semua folder di atas.
2. Tidak menghapus folder jika sudah ada.
3. Tidak overwrite file existing.
4. Membuat `README.md` pendek di setiap folder utama.
5. Menyimpan struktur yang dibuat ke `folder_structure_manifest.json`.

## Copy Policy

Default:

```text
COPY_ONLY
```

Jangan MOVE secara default.

Jika file tujuan sudah ada:

```text
- Jika ukuran dan nama sama → skip duplicate.
- Jika nama sama ukuran beda → tambahkan suffix _copy1.
- Catat konflik ke copy_conflicts.csv.
```

## Folder Recommendation

Setiap file hasil klasifikasi harus punya `recommended_folder`.

Contoh:

```text
ramadhan_only + imsak → 05_ADZAN_DAN_MUSIMAN\RAMADHAN_ONLY\IMSAK
adzan + maghrib → 05_ADZAN_DAN_MUSIMAN\ADZAN\MAGHRIB
station_id/top of hour → 02_JINGLE_SWEEPER_ID\TOP_OF_HOUR
podcast → 06_PROGRAM_ACARA\PODCAST\REVIEW atau AKTIF
unknown → 09_REVIEW_KARANTINA\UNKNOWN
```

## Acceptance Criteria

- Struktur baru dibuat lengkap.
- File lama tetap aman.
- Semua file copy tercatat.
- File ragu-ragu tidak masuk folder aktif.
- Folder Ramadhan/adzan terpisah total dari musik reguler.
