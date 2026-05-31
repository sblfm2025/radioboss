# 06 — Playlist Audit and Rebuild

## Tujuan

Mengaudit playlist lama RadioBOSS dan membuat playlist baru yang bersih.

## Playlist Extensions

```text
.m3u
.m3u8
.pls
.txt jika formatnya berisi daftar path audio
```

## Playlist Audit

Untuk setiap playlist:

```text
- path playlist
- nama file
- total item
- item ditemukan
- item hilang
- item Ramadhan
- item adzan
- item ILM
- item iklan
- item podcast/event
- path folder lama
- status
- rekomendasi
```

## Playlist Status

```text
SAFE_REFERENCE
NEEDS_REVIEW
DANGEROUS
BROKEN_PATH
ARCHIVE_ONLY
UNKNOWN
```

## Dangerous Conditions

Playlist `DANGEROUS` jika:

- berisi adzan,
- berisi imsak/sahur/buka puasa/takbiran,
- berisi shalawat Ramadhan di playlist reguler,
- berisi podcast panjang dalam playlist musik,
- banyak path hilang,
- merujuk folder download/cache/operator liar.

## Report

`playlist_lama_report.csv`:

```csv
playlist_file,total_items,missing_items,ramadhan_items,adzan_items,podcast_items,status,recommendation
```

`playlist_items_detail.csv`:

```csv
playlist_file,item_path,exists,detected_type,risk,recommendation
```

## Rebuild Playlist Baru

Aplikasi harus membuat playlist `.m3u8` dari struktur fresh.

Output:

```text
D:\RADIO_SBL_FRESH\07_PLAYLIST_BARU\REGULER_HARIAN\
D:\RADIO_SBL_FRESH\08_RADIOBOSS_EXPORT\M3U8\
```

## Format File M3U8

```text
#EXTM3U
D:\RADIO_SBL_FRESH\02_JINGLE_SWEEPER_ID\TOP_OF_HOUR\SBL_TOH_01.mp3
D:\RADIO_SBL_FRESH\01_MUSIC_ACTIVE\A_POWER_CURRENT_HIT\Artist - Judul.mp3
D:\RADIO_SBL_FRESH\02_JINGLE_SWEEPER_ID\SWEEPER_PENDEK\SBL_SWEEPER_01.mp3
```

## Playlist Naming Standard

```text
YYYY-MM-DD_HHMM_CLOCK_NAME.m3u8
```

Contoh:

```text
2026-06-01_0500_SALAM_SUBUH.m3u8
2026-06-01_0700_SEMANGAT_PAGI.m3u8
2026-06-01_1300_ILM_EDUKASI.m3u8
2026-06-01_1800_RELIGI.m3u8
```

## Rebuild Rules

### Reguler

Boleh mengambil:

```text
A_POWER_CURRENT_HIT
B_HOT_ROTATION
C_MEDIUM_ROTATION
D_GOLD_RECURRENT
E_NOSTALGIA
F_DANGDUT
H_LAGU_DAERAH_LOKAL
```

Tidak boleh mengambil:

```text
RAMADHAN_ONLY
ADZAN
PODCAST
SPECIAL_EVENT
LIPUTAN_KHUSUS
IKLAN SELESAI
ILM KADALUARSA
REVIEW_KARANTINA
```

### Religi Reguler

Boleh:

```text
G_RELIGI_REGULER
ILM sosial/religi aktif
jingle religi reguler
```

Tidak boleh:

```text
IMSAK
SAHUR
BUKA_PUASA
TARAWIH
SHALAWAT_RAMADHAN
TAKBIRAN
```

## Manifest Per Playlist

Setiap export playlist harus punya metadata di `manifest.json`:

```json
{
  "playlistFile": "2026-06-01_0700_SEMANGAT_PAGI.m3u8",
  "clockId": "CLOCK_0700_SEMANGAT_PAGI",
  "totalItems": 14,
  "blockedItems": 0,
  "warnings": [],
  "status": "READY"
}
```

## Acceptance Criteria

- Playlist baru tidak berisi adzan/Ramadhan-only.
- Playlist baru hanya mengambil file approved.
- Semua file yang masuk playlist ada di disk.
- Semua playlist punya manifest.
- Playlist lama tidak dihapus, hanya dilaporkan/diarsipkan.
