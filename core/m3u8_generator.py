import os
import json
import csv
import shutil
from db.database import get_db_connection
from core.fresh_folder_builder import load_fresh_root

def generate_fresh_playlists():
    """
    Membuat file playlist .m3u8 baru yang bersih dan steril untuk RadioBOSS.
    Memblokir file Ramadhan, adzan, kotor, dan review dari daftar putar siaran reguler.
    """
    fresh_root = load_fresh_root()
    playlist_dest_dir = os.path.join(fresh_root, "07_PLAYLIST_BARU")
    os.makedirs(playlist_dest_dir, exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Ambil file audio yang berstatus aman (MIGRATED atau APPROVED)
    cursor.execute("""
        SELECT original_path, file_name, detected_type, risk_level, status 
        FROM file_index 
        WHERE status IN ('MIGRATED', 'APPROVED')
    """)
    rows = cursor.fetchall()
    
    # Kelompokkan file audio berdasarkan tipenya untuk menyusun playlist secara teratur
    music_tracks = []
    jingle_tracks = []
    ilm_tracks = []
    religi_tracks = []
    
    for row in rows:
        path = row['original_path']
        name = row['file_name']
        dtype = row['detected_type']
        
        # Blokir materi musiman Ramadhan, adzan, dan file mencurigakan dari playlist reguler
        if dtype in {"ramadhan_only", "adzan"} or row['status'] in {"REVIEW", "DANGEROUS"}:
            continue
            
        if dtype == "ilm_spot":
            ilm_tracks.append(path)
        elif dtype == "jingle_sweeper":
            jingle_tracks.append(path)
        elif "religi" in name.lower() or "sholawat" in name.lower():
            religi_tracks.append(path)
        else:
            music_tracks.append(path)
            
    # Fallback dummy tracks jika database kosong demi kemudahan testing QA stasiun radio
    if not music_tracks:
        music_tracks = [os.path.join(fresh_root, "01_MUSIC_ACTIVE", "Pop_Reguler_Dummy.mp3")]
    if not jingle_tracks:
        jingle_tracks = [os.path.join(fresh_root, "02_JINGLE_SWEEPER_ID", "Station_ID_Dummy.mp3")]
    if not ilm_tracks:
        ilm_tracks = [os.path.join(fresh_root, "03_ILM", "SP4N_Lapor_Dummy.mp3")]
    if not religi_tracks:
        religi_tracks = [os.path.join(fresh_root, "01_MUSIC_ACTIVE", "Religi_Reguler_Dummy.mp3")]
        
    playlists_to_build = {
        "0500_SALAM_SUBUH.m3u8": [
            jingle_tracks[0],
            religi_tracks[0],
            jingle_tracks[min(1, len(jingle_tracks)-1)],
            religi_tracks[min(1, len(religi_tracks)-1)]
        ],
        "0700_SEMANGAT_PAGI.m3u8": [
            jingle_tracks[0],
            music_tracks[0],
            music_tracks[min(1, len(music_tracks)-1)],
            jingle_tracks[min(1, len(jingle_tracks)-1)],
            music_tracks[min(2, len(music_tracks)-1)]
        ],
        "1300_ILM_EDUKASI.m3u8": [
            jingle_tracks[0],
            ilm_tracks[0],
            music_tracks[0],
            jingle_tracks[min(1, len(jingle_tracks)-1)],
            ilm_tracks[min(1, len(ilm_tracks)-1)]
        ],
        "1800_RELIGI_REGULER.m3u8": [
            jingle_tracks[0],
            religi_tracks[0],
            religi_tracks[min(1, len(religi_tracks)-1)],
            jingle_tracks[min(1, len(jingle_tracks)-1)]
        ]
    }
    
    export_manifest = {
        "export_date": os.popen('date /t').read().strip() + " " + os.popen('time /t').read().strip(),
        "playlists": {}
    }
    
    generated_count = 0
    
    for filename, tracks in playlists_to_build.items():
        playlist_path = os.path.join(playlist_dest_dir, filename)
        
        try:
            with open(playlist_path, 'w', encoding='utf-8') as f:
                f.write("#EXTM3U\n")
                for track in tracks:
                    track_name = os.path.basename(track)
                    f.write(f"#EXTINF:-1,{track_name}\n")
                    f.write(f"{track}\n")
                    
            export_manifest["playlists"][filename] = {
                "full_path": playlist_path,
                "total_items": len(tracks),
                "status": "GENERATED"
            }
            generated_count += 1
        except Exception as e:
            export_manifest["playlists"][filename] = {
                "full_path": playlist_path,
                "total_items": 0,
                "status": f"FAILED: {e}"
            }
            
    # Tulis file manifest export ke output/playlists/
    manifest_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'playlists')
    os.makedirs(manifest_dir, exist_ok=True)
    
    try:
        with open(os.path.join(manifest_dir, "export_manifest.json"), 'w', encoding='utf-8') as js_f:
            json.dump(export_manifest, js_f, indent=2, ensure_ascii=False)
            
        # Copy playlist hasil ke direktori output/playlists/ stasiun radio demi kemudahan operator
        for filename in playlists_to_build.keys():
            src_pl = os.path.join(playlist_dest_dir, filename)
            dest_pl = os.path.join(manifest_dir, filename)
            if os.path.exists(src_pl):
                shutil.copy2(src_pl, dest_pl)
    except Exception as e:
         print(f"Error saving playlist export manifest: {e}")
         
    conn.close()
    return generated_count

if __name__ == "__main__":
    from db.database import init_db
    init_db()
    res = generate_fresh_playlists()
    print("Playlist Builder selesai. Berhasil membuat", res, "playlist baru.")
