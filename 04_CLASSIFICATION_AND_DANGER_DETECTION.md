# 04 — Classification and Danger Detection

## Tujuan

Mengklasifikasikan file dan playlist agar tidak ada materi berbahaya masuk playlist reguler.

## Detected Types

```text
music
jingle
sweeper
station_id
program_bumper
program_promo
ilm
ad
adzan
religi_regular
ramadhan_only
eid_only
podcast
special_event
special_coverage
live_report
recorded_interview
youtube_relay
external_stream
whatsapp_call
zoom_meeting
discord_call
special_song
emergency_fallback
review
unknown
```

## Status File

```text
APPROVED
REVIEW
BLOCK_REGULAR
SPECIAL_SCHEDULE_ONLY
ADZAN_EVENT_ONLY
ARCHIVE_RECOMMENDED
EXPIRED
BROKEN
UNKNOWN
```

## Keyword Rules

`config/keyword_rules.json`:

```json
{
  "ramadhanOnly": [
    "ramadhan", "ramadan", "imsak", "sahur", "buka puasa",
    "berbuka", "tarawih", "takjil", "ngabuburit", "kultum ramadhan",
    "shalawat ramadhan"
  ],
  "eidOnly": ["idul fitri", "lebaran", "takbiran", "idul adha", "qurban"],
  "adzan": ["adzan", "azan", "subuh", "dzuhur", "zuhur", "ashar", "asar", "maghrib", "magrib", "isya"],
  "jingle": ["jingle", "station id", "sbl id", "toh", "top of hour"],
  "sweeper": ["sweeper", "liner", "stinger"],
  "ilm": ["ilm", "iklan layanan masyarakat", "layanan masyarakat"],
  "ad": ["iklan", "ads", "spot", "commercial", "sponsor"],
  "podcast": ["podcast", "episode", "eps"],
  "specialEvent": ["special event", "event", "on stage", "hut", "festival"],
  "coverage": ["liputan", "reportase", "live report", "wawancara", "interview"],
  "liveSource": ["youtube", "zoom", "discord", "meet", "whatsapp", "relay"]
}
```

## Classification Rules

### Ramadhan-only

Jika path/nama file mengandung keyword Ramadhan:

```text
detected_type = ramadhan_only
status = BLOCK_REGULAR
risk_level = HIGH
```

Tidak boleh masuk playlist reguler.

### Adzan

Jika mengandung keyword adzan/waktu shalat:

```text
detected_type = adzan
status = ADZAN_EVENT_ONLY
risk_level = HIGH
```

Tidak boleh masuk playlist acak.

### ILM

Jika mengandung keyword ILM:

```text
detected_type = ilm
status = REVIEW jika tanggal aktif tidak jelas
risk_level = MEDIUM
```

### Iklan

Jika mengandung keyword iklan/ads/spot/commercial:

```text
detected_type = ad
status = REVIEW
risk_level = MEDIUM
```

Jika mengandung `selesai`, `expired`, `lama`, atau tanggal selesai lewat:

```text
status = EXPIRED
risk_level = HIGH
```

### Podcast

Jika mengandung `podcast`, `episode`, `eps`:

```text
detected_type = podcast
status = REVIEW
blocked_from_regular = true
```

### Event / Liputan

Jika mengandung `liputan`, `event`, `wawancara`, `live report`:

```text
detected_type = special_coverage atau special_event
status = REVIEW
blocked_from_regular = true
```

## Dangerous Playlist Item Rules

Playlist dianggap `DANGEROUS` jika:

- mengandung `ramadhan_only`,
- mengandung `adzan`,
- mengandung `eid_only`,
- mengandung item path hilang lebih dari ambang batas,
- mengandung kombinasi lagu + adzan + ILM + podcast dalam satu playlist tanpa struktur jelas.

## Risk Scoring

```python
score = 0
if is_ramadhan: score += 50
if is_adzan: score += 50
if path_missing: score += 30
if is_expired_ad: score += 25
if is_podcast_in_regular_playlist: score += 25
if from_download_or_cache: score += 10

if score >= 70: risk = "CRITICAL"
elif score >= 40: risk = "HIGH"
elif score >= 15: risk = "MEDIUM"
else: risk = "LOW"
```

## Reports

```text
dangerous_items.csv
ramadhan_adzan_report.csv
expired_ads_report.csv
podcast_special_event_report.csv
classification_review.csv
```

## Acceptance Criteria

- File Ramadhan tidak masuk kategori reguler.
- Adzan selalu ditandai event-only.
- Podcast/event tidak masuk rotasi musik.
- Semua klasifikasi ragu masuk REVIEW.
- Semua hasil bisa diedit manual oleh admin sebelum copy/export.
