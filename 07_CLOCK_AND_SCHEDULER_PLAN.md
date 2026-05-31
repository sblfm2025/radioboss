# 07 — Clock and Scheduler Plan

## Tujuan

Menyiapkan clock program dan rencana scheduler RadioBOSS baru.

Aplikasi tidak perlu menulis langsung ke scheduler RadioBOSS pada versi awal. Cukup menghasilkan plan yang bisa diinput manual oleh admin.

## Clock Default

```text
CLOCK_0500_SALAM_SUBUH
CLOCK_0700_SEMANGAT_PAGI
CLOCK_0800_PROGRAM_PAGI
CLOCK_1000_LASINRANG_PRENEUR
CLOCK_1130_KELUARGA_BERDAYA
CLOCK_1300_ILM_EDUKASI
CLOCK_1400_INFO_PINRANG
CLOCK_1600_PROGRAM_SORE
CLOCK_1800_RELIGI
CLOCK_2000_PROGRAM_MALAM
CLOCK_2200_LAGU_TERBAIK
CLOCK_2300_OFF_RELAY_SAFE
CLOCK_LIPUTAN_KHUSUS
CLOCK_SPECIAL_EVENT
CLOCK_PODCAST
CLOCK_LIVE_CALL
CLOCK_YOUTUBE_RELAY
CLOCK_ONLINE_MEETING
CLOCK_EMERGENCY_FALLBACK
```

## Clock Template JSON

`config/clock_templates.json`:

```json
{
  "CLOCK_0700_SEMANGAT_PAGI": {
    "name": "Semangat Pagi",
    "start": "07:00",
    "end": "08:00",
    "allowedCategories": [
      "A_POWER_CURRENT_HIT",
      "B_HOT_ROTATION",
      "C_MEDIUM_ROTATION",
      "H_LAGU_DAERAH_LOKAL"
    ],
    "blockedTags": [
      "RAMADHAN_ONLY",
      "ADZAN",
      "PODCAST",
      "SPECIAL_EVENT",
      "REVIEW"
    ],
    "inserts": [
      {"type": "TOP_OF_HOUR", "atMinute": 0},
      {"type": "SWEEPER", "everySongs": 3},
      {"type": "ILM", "atMinute": 18, "optional": true}
    ],
    "fallback": "EMERGENCY_GENERAL.m3u8"
  }
}
```

## Clock Structure Examples

### CLOCK_0500_SALAM_SUBUH

```text
05:00 Bumper Salam Subuh
05:01 Station ID lembut
05:02 Religi reguler
05:08 Doa pagi / tausiah pendek
05:15 Religi reguler
05:22 ILM sosial/kesehatan aktif
05:25 Religi reguler
05:35 Konten inspiratif
05:45 Religi reguler
05:55 Sweeper menuju jam 06
06:00 Station ID
06:01 Religi reguler
06:55 Promo Semangat Pagi
```

### CLOCK_1300_ILM_EDUKASI

```text
13:00 Station ID
13:01 ILM 1
13:03 Lagu ringan
13:08 Tips kesehatan/edukasi
13:12 ILM 2
13:15 Lagu ringan
13:22 Info publik
13:25 Sweeper
13:34 ILM 3
13:55 Promo program berikutnya
```

### CLOCK_1800_RELIGI

```text
18:00 Bumper religi
18:02 Religi reguler
18:08 Tausiah/pesan moral
18:20 Religi reguler
18:28 Station ID
18:30 Konten dakwah/inspirasi
19:30 ILM sosial/religi
19:55 Promo program malam
```

## Scheduler Plan Output

`radioboss_scheduler_plan.csv`:

```csv
time,event_name,action,target_file,notes,status
05:00,CLOCK_0500_SALAM_SUBUH,load,D:\RADIO_SBL_FRESH\08_RADIOBOSS_EXPORT\M3U8\TODAY_0500_SALAM_SUBUH.m3u8,Playlist religi reguler,READY
07:00,CLOCK_0700_SEMANGAT_PAGI,load,D:\RADIO_SBL_FRESH\08_RADIOBOSS_EXPORT\M3U8\TODAY_0700_SEMANGAT_PAGI.m3u8,Playlist pagi,READY
13:00,CLOCK_1300_ILM_EDUKASI,load,D:\RADIO_SBL_FRESH\08_RADIOBOSS_EXPORT\M3U8\TODAY_1300_ILM_EDUKASI.m3u8,ILM edukasi,READY
18:00,CLOCK_1800_RELIGI,load,D:\RADIO_SBL_FRESH\08_RADIOBOSS_EXPORT\M3U8\TODAY_1800_RELIGI.m3u8,Religi reguler,READY
```

## Scheduler Markdown Checklist

Aplikasi juga harus membuat:

```text
08_RADIOBOSS_EXPORT\SCHEDULER_PLAN\setup_scheduler_manual.md
```

Isi:

```text
1. Buka RadioBOSS Scheduler.
2. Disable event lama yang masuk laporan dangerous.
3. Buat event baru sesuai CSV.
4. Gunakan action load playlist.
5. Arahkan ke file .m3u8 hasil export.
6. Test setiap event secara manual.
```

## Rules

- Adzan dibuat scheduler khusus, bukan clock acak.
- Ramadhan event default nonaktif.
- Special event wajib tanggal mulai dan selesai.
- Live source wajib fallback.
- Playlist reguler wajib bebas Ramadhan/adzan/podcast/event.

## Acceptance Criteria

- Semua clock default tersedia.
- Scheduler plan bisa diekspor CSV dan MD.
- Tidak ada event berbahaya di plan reguler.
- Setiap event punya target playlist/fallback.
