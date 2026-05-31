# 10 — Emergency Fallback

## Tujuan

Mencegah dead air saat relay, call, meeting, event, atau playlist gagal.

## Folder

```text
07_PLAYLIST_BARU\EMERGENCY\
├── EMERGENCY_GENERAL.m3u8
├── EMERGENCY_RELAY.m3u8
├── EMERGENCY_CALL_FAILED.m3u8
├── EMERGENCY_EVENT_DELAY.m3u8
├── EMERGENCY_NETWORK_DOWN.m3u8
└── EMERGENCY_OFFAIR_SAFE.m3u8
```

## Isi Fallback

Fallback harus berisi aset aman:

```text
- station ID
- lagu aman
- sweeper
- ILM umum aktif
- promo program
```

Tidak boleh berisi:

```text
- adzan
- Ramadhan-only
- iklan expired
- podcast panjang
- event lama
- file review
```

## Fallback Types

### EMERGENCY_GENERAL

Untuk error umum.

### EMERGENCY_RELAY

Untuk YouTube/external stream putus.

### EMERGENCY_CALL_FAILED

Untuk WhatsApp/Zoom/Discord gagal.

### EMERGENCY_EVENT_DELAY

Untuk event molor/delay.

### EMERGENCY_NETWORK_DOWN

Untuk koneksi internet putus.

### EMERGENCY_OFFAIR_SAFE

Untuk jeda/off-air aman.

## Manifest

`emergency_fallback_manifest.json`:

```json
{
  "fallbacks": [
    {
      "id": "EMERGENCY_RELAY",
      "file": "EMERGENCY_RELAY.m3u8",
      "totalItems": 12,
      "durationEstimateMinutes": 45,
      "status": "READY",
      "warnings": []
    }
  ]
}
```

## Generation Rules

- Minimal durasi fallback 30 menit.
- Ideal durasi fallback 60–120 menit.
- Tidak boleh ada file missing.
- Tidak boleh ada item dangerous.
- Semua fallback harus diuji dengan parser sebelum ditandai READY.

## UI Requirements

Halaman `Emergency Fallback`:

```text
- Daftar fallback
- Total item
- Estimasi durasi
- Status READY/NOT_READY
- Warning
- Tombol Generate
- Tombol Open Playlist
- Tombol Export Report
```

## Report

`emergency_fallback_report.csv`:

```csv
fallback_id,file,total_items,missing_items,danger_items,status
EMERGENCY_RELAY,EMERGENCY_RELAY.m3u8,12,0,0,READY
EMERGENCY_CALL_FAILED,EMERGENCY_CALL_FAILED.m3u8,10,0,0,READY
```

## Acceptance Criteria

- Semua live source wajib punya fallback.
- Fallback bebas adzan/Ramadhan-only/review.
- Fallback punya estimasi durasi.
- Fallback punya manifest.
- Fallback bisa diputar manual di RadioBOSS.
