# 09 — Live Source and Call Workflow

## Tujuan

Menyiapkan semua sumber audio non-file agar tidak dibuat dadakan oleh operator.

Scope:

```text
- Relay YouTube
- External stream
- WhatsApp voice/video call
- Discord
- Zoom Meeting
- Google Meet
- Input mixer / audio interface
- Virtual audio routing
```

## Folder

```text
06_PROGRAM_ACARA\
├── RELAY\
├── LIVE_CALL\
├── YOUTUBE_RELAY\
└── ZOOM_DISCORD_MEETING\
```

## Categories

```text
youtube_relay
external_stream_relay
whatsapp_call
discord_call
zoom_meeting
google_meet
phone_patch
mixer_input
virtual_audio_input
```

## Relay YouTube

### Data Model

```json
{
  "type": "youtube_relay",
  "title": "Relay YouTube Acara Pemda",
  "url": "https://youtube.com/...",
  "date": "2026-06-01",
  "startTime": "09:00",
  "endTime": "11:00",
  "audioRoute": "ROUTE_BROWSER_YOUTUBE",
  "fallbackPlaylist": "EMERGENCY_RELAY.m3u8",
  "status": "scheduled"
}
```

### Checklist

```text
[ ] Link YouTube sudah diuji.
[ ] Audio YouTube masuk ke jalur mixer/virtual cable.
[ ] Volume YouTube sudah disetarakan.
[ ] Notifikasi browser dimatikan.
[ ] Browser hanya membuka tab yang diperlukan.
[ ] Bumper relay tersedia.
[ ] Playlist fallback tersedia.
[ ] Operator tahu tombol balik ke siaran reguler.
```

## WhatsApp Call

### Checklist

```text
[ ] Nomor/nama narasumber sudah siap.
[ ] Koneksi internet stabil.
[ ] Notifikasi WhatsApp dimatikan.
[ ] Audio WhatsApp masuk mixer/virtual cable.
[ ] Mic penyiar tidak menyebabkan echo ke narasumber.
[ ] Level suara narasumber sudah dites.
[ ] Bumper telepon tersedia.
[ ] Fallback lagu/ILM tersedia jika panggilan gagal.
[ ] Operator tahu cara mute/unmute.
[ ] Rekaman aktif jika diperlukan.
```

## Zoom / Discord / Google Meet

### Data Model

```json
{
  "type": "zoom_meeting",
  "title": "Dialog Publik Online",
  "platform": "Zoom",
  "meetingTime": "2026-06-01 20:00",
  "host": "Operator SBL",
  "audioRoute": "ROUTE_ZOOM_MEETING",
  "fallbackPlaylist": "EMERGENCY_EVENT_DELAY.m3u8",
  "recordingRequired": true,
  "status": "scheduled"
}
```

### Checklist

```text
[ ] Link meeting valid.
[ ] Akun host sudah login.
[ ] Nama akun profesional.
[ ] Audio output meeting diarahkan ke mixer/virtual cable.
[ ] Mic penyiar masuk ke meeting jika perlu.
[ ] Echo cancellation diuji.
[ ] Semua notifikasi dimatikan.
[ ] Narasumber sudah tes audio.
[ ] Recording disiapkan jika perlu.
[ ] Fallback playlist tersedia.
```

## Audio Routing Profiles

Aplikasi tidak harus mengatur soundcard secara langsung, tetapi wajib menyimpan profil routing.

`audio_routing_profiles.json`:

```json
{
  "audioRoutingProfiles": [
    {
      "id": "ROUTE_BROWSER_YOUTUBE",
      "name": "Browser YouTube ke RadioBOSS",
      "sourceApp": "Chrome/Edge",
      "inputDevice": "Virtual Audio Cable / Mixer Channel",
      "outputDevice": "RadioBOSS Input / Mixer",
      "useCase": ["youtube_relay", "external_stream"]
    },
    {
      "id": "ROUTE_WHATSAPP_CALL",
      "name": "WhatsApp Call ke Mixer",
      "sourceApp": "WhatsApp Desktop",
      "inputDevice": "Virtual Audio Cable / Mixer Channel",
      "outputDevice": "RadioBOSS / Encoder",
      "useCase": ["whatsapp_call", "live_call"]
    }
  ]
}
```

## Live Source Plan Report

`live_source_plan.csv`:

```csv
date,time,type,title,source,audio_route,fallback,status
2026-06-15,09:00,youtube_relay,Relay HUT Pinrang,YouTube,ROUTE_BROWSER_YOUTUBE,EMERGENCY_RELAY.m3u8,scheduled
2026-06-15,10:30,whatsapp_call,Wawancara Narasumber,WhatsApp,ROUTE_WHATSAPP_CALL,EMERGENCY_CALL_FAILED.m3u8,scheduled
```

## Hard Rules

1. Relay YouTube tidak boleh dibuat tanpa fallback.
2. Live call tidak boleh dibuat tanpa audio route.
3. Online meeting wajib punya checklist audio.
4. Event sumber live wajib punya jam mulai dan selesai.
5. Jika route belum terisi, status `NOT_READY`.

## Acceptance Criteria

- Bisa membuat plan YouTube relay.
- Bisa membuat plan WhatsApp/Zoom/Discord.
- Semua live source punya fallback.
- Semua live source punya checklist.
- Ada laporan siap cetak/operator.
