# 08 — Special Programs, Podcast, and Events

## Tujuan

Menyiapkan workflow khusus agar liputan khusus, special event, podcast, talkshow, dan lagu khusus tidak tercampur dengan playlist reguler.

## Folder Khusus

```text
06_PROGRAM_ACARA\
├── LIPUTAN_KHUSUS\
├── SPECIAL_EVENT\
├── PODCAST\
├── TALKSHOW\
└── CADANGAN_PROGRAM\
```

## Kategori

```text
special_coverage
special_event
podcast
talkshow
live_report
recorded_interview
program_bumper
program_promo
special_song
program_archive
```

## Status

```text
scheduled
active
finished
archive
review
blocked
```

## Liputan Khusus

### Folder

```text
06_PROGRAM_ACARA\LIPUTAN_KHUSUS\
├── AKTIF\
├── TERJADWAL\
├── SELESAI\
├── ARSIP\
├── BUMPER_LIPUTAN\
├── LIVE_REPORT\
├── WAWANCARA\
└── REVIEW\
```

### Rules

- Tidak boleh masuk rotasi musik reguler.
- Wajib punya judul liputan.
- Jika sudah selesai, rekomendasikan ke `SELESAI` atau `ARSIP`.
- Jika tidak punya tanggal, status `REVIEW`.

### Manifest

```json
{
  "type": "special_coverage",
  "title": "Liputan Khusus HUT Pinrang",
  "eventDate": "2026-06-15",
  "status": "scheduled",
  "blockedFromRegular": true,
  "fallbackPlaylist": "EMERGENCY_RELAY.m3u8"
}
```

## Special Event

### Folder

```text
06_PROGRAM_ACARA\SPECIAL_EVENT\AKTIF\2026-06-15_HUT_PINRANG\
├── 01_BUMPER\
├── 02_LAGU_KHUSUS\
├── 03_INSERT\
├── 04_RELAY\
├── 05_WAWANCARA\
├── 06_ILM_SPONSOR\
├── 07_FALLBACK\
└── event_manifest.json
```

### Rules

- Wajib punya tanggal mulai.
- Wajib punya tanggal selesai.
- Bumper event tidak boleh masuk jingle reguler.
- Promo event dianggap kadaluarsa setelah event selesai.
- Playlist event disimpan terpisah.

### Output

```text
2026-06-15_HUT_PINRANG_MAIN.m3u8
2026-06-15_HUT_PINRANG_FALLBACK.m3u8
2026-06-15_HUT_PINRANG_CHECKLIST.md
2026-06-15_HUT_PINRANG_MANIFEST.json
```

## Podcast

### Folder

```text
06_PROGRAM_ACARA\PODCAST\
├── AKTIF\
├── EPISODE_BARU\
├── EPISODE_TAYANG_ULANG\
├── ARSIP\
├── BUMPER_PODCAST\
├── PROMO_PODCAST\
└── REVIEW\
```

### Rules

- Podcast tidak boleh masuk playlist musik reguler.
- Podcast hanya boleh masuk clock podcast/talkshow.
- Episode baru status awal `REVIEW`.
- Episode tayang ulang harus punya tanggal/jam.
- Podcast lama masuk `ARSIP`.

### Playlist Podcast

```text
#EXTM3U
D:\RADIO_SBL_FRESH\06_PROGRAM_ACARA\PODCAST\BUMPER_PODCAST\SBL_PODCAST_OPENING.mp3
D:\RADIO_SBL_FRESH\06_PROGRAM_ACARA\PODCAST\AKTIF\SIPORIO\Podcast_Siporio_Eps001.mp3
D:\RADIO_SBL_FRESH\02_JINGLE_SWEEPER_ID\REGULAR_JINGLE\SBL_ID_PENDEK.mp3
D:\RADIO_SBL_FRESH\06_PROGRAM_ACARA\PODCAST\PROMO_PODCAST\Promo_Episode_Berikutnya.mp3
```

## Lagu Khusus

Folder:

```text
06_PROGRAM_ACARA\SPECIAL_EVENT\LAGU_KHUSUS\
├── AKTIF\
├── EVENT_TERTENTU\
├── REQUEST_KHUSUS\
├── ARSIP\
└── REVIEW\
```

Rules:

- Tidak masuk rotasi harian otomatis.
- Harus punya alasan penggunaan.
- Boleh masuk playlist event tertentu.
- Setelah event selesai, status `ARSIP` atau `REVIEW`.

## Reports

```text
special_event_report.csv
podcast_report.csv
coverage_report.csv
special_song_report.csv
program_archive_report.csv
```

## Acceptance Criteria

- Podcast/event/liputan tidak masuk playlist reguler.
- Setiap event punya manifest.
- Event selesai terdeteksi untuk arsip.
- Lagu khusus hanya masuk playlist khusus.
