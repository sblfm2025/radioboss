import os
import json
from db.database import get_db_connection

def load_fresh_root():
    """Mengambil jalur folder fresh root dari konfigurasi."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'app_config.json')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("freshRoot", "D:\\RADIO_SBL_FRESH")
        except Exception:
            pass
    return "D:\\RADIO_SBL_FRESH"

def build_fresh_structure():
    """
    Membangun struktur direktori steril lengkap di bawah fresh root
    dan mengekspor file folder_structure_manifest.json.
    """
    fresh_root = load_fresh_root()
    
    # Daftar subdirektori yang wajib dibuat untuk fresh reset
    folders = [
        "00_ARSIP_LAMA",
        "01_MUSIC_ACTIVE",
        "02_JINGLE_SWEEPER_ID",
        "03_ILM",
        "04_IKLAN",
        "05_ADZAN_DAN_MUSIMAN",
        "05_ADZAN_DAN_MUSIMAN\\ADZAN",
        "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY",
        "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY\\IMSAK",
        "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY\\SAHUR",
        "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY\\BUKA_PUASA",
        "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY\\HIKMAH_PUASA",
        "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY\\KULTUM_RAMADHAN",
        "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY\\SHALAWAT_RAMADHAN",
        "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY\\JINGLE_RAMADHAN",
        "06_PROGRAM_ACARA",
        "07_PLAYLIST_BARU",
        "08_RADIOBOSS_EXPORT",
        "09_LAPORAN_RESET"
    ]
    
    manifest_data = {
        "fresh_root": fresh_root,
        "created_at": os.popen('date /t').read().strip() + " " + os.popen('time /t').read().strip(),
        "structure": {}
    }
    
    created_folders = []
    
    for f in folders:
        full_path = os.path.join(fresh_root, f)
        os.makedirs(full_path, exist_ok=True)
        created_folders.append(full_path)
        
        # Penjelasan peruntukan folder untuk manifest
        desc = "Folder penataan aset"
        if f == "00_ARSIP_LAMA":
            desc = "Arsip cadangan untuk berkas mentah lama stasiun radio sebelum reset."
        elif f == "01_MUSIC_ACTIVE":
            desc = "Katalog lagu musik reguler stasiun radio yang bersih dan siap siar."
        elif f == "02_JINGLE_SWEEPER_ID":
            desc = "Jingle resmi program stasiun radio, Station ID, Bed music, dan Sweeper."
        elif f == "03_ILM":
            desc = "Iklan Layanan Masyarakat resmi (SP4N Lapor, Stop Bullying, Anti Narkoba, Anti Judol)."
        elif f == "04_IKLAN":
            desc = "Spot Iklan sponsor komersial aktif stasiun radio."
        elif f == "05_ADZAN_DAN_MUSIMAN":
            desc = "Materi khusus adzan wilayah setempat dan folder arsip seasonal."
        elif "RAMADHAN_ONLY" in f:
            desc = f"Folder khusus seasonal Ramadhan: {f.split('\\')[-1]}."
        elif f == "06_PROGRAM_ACARA":
            desc = "Materi program rekaman siaran stasiun radio."
        elif f == "07_PLAYLIST_BARU":
            desc = "Daftar putar (playlist) baru berformat .m3u8 hasil generate reset."
        elif f == "08_RADIOBOSS_EXPORT":
            desc = "Hasil ekspor scheduler plan siap impor manual ke RadioBOSS."
        elif f == "09_LAPORAN_RESET":
            desc = "Laporan before/after reset, daftar missing path, dan checklist setup."
            
        manifest_data["structure"][f] = {
            "full_path": full_path,
            "description": desc,
            "status": "CREATED"
        }
        
    # Tulis file manifest JSON ke fresh root
    manifest_path = os.path.join(fresh_root, "folder_structure_manifest.json")
    try:
        with open(manifest_path, 'w', encoding='utf-8') as js_f:
            json.dump(manifest_data, js_f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing manifest to fresh root: {e}")
        
    # Juga tulis manifest JSON ke folder output/manifests/ aplikasi
    app_manifest_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'manifests')
    os.makedirs(app_manifest_dir, exist_ok=True)
    try:
        with open(os.path.join(app_manifest_dir, "folder_structure_manifest.json"), 'w', encoding='utf-8') as app_js_f:
            json.dump(manifest_data, app_js_f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing manifest to app outputs: {e}")
        
    return fresh_root, len(created_folders)

if __name__ == "__main__":
    res = build_fresh_structure()
    print(f"Fresh Structure sukses dibangun di: {res[0]} (Total {res[1]} folder)")
