import os
import csv
from db.database import get_db_connection
from core.fresh_folder_builder import load_fresh_root

def generate_scheduler_plan():
    """
    Menyusun rencana penjadwalan baru yang bersih untuk diimpor atau dikonfigurasi
    secara manual oleh admin stasiun radio di RadioBOSS.
    """
    fresh_root = load_fresh_root()
    playlist_dir = os.path.join(fresh_root, "07_PLAYLIST_BARU")
    adzan_file = os.path.join(fresh_root, "05_ADZAN_DAN_MUSIMAN", "ADZAN", "Adzan_Maghrib_SBL.mp3")
    
    # Rencana event scheduler steril baru stasiun radio SBL
    new_plan = [
        {
            "event_group": "01_HARI_REGULER",
            "event_name": "Salam Subuh Pembuka",
            "time": "05:00:00",
            "command_type": "load",
            "target_path": os.path.join(playlist_dir, "0500_SALAM_SUBUH.m3u8"),
            "risk_level": "LOW",
            "status": "READY",
            "notes": "Memutar lagu religi pembuka pagi hari stasiun radio secara bersih."
        },
        {
            "event_group": "01_HARI_REGULER",
            "event_name": "Semangat Pagi Rotasi",
            "time": "07:00:00",
            "command_type": "load",
            "target_path": os.path.join(playlist_dir, "0700_SEMANGAT_PAGI.m3u8"),
            "risk_level": "LOW",
            "status": "READY",
            "notes": "Lagu pop Indonesia/indie pagi hari penambah semangat pendengar."
        },
        {
            "event_group": "01_HARI_REGULER",
            "event_name": "ILM Edukasi Publik",
            "time": "13:00:00",
            "command_type": "load",
            "target_path": os.path.join(playlist_dir, "1300_ILM_EDUKASI.m3u8"),
            "risk_level": "LOW",
            "status": "READY",
            "notes": "Rotasi Iklan Layanan Masyarakat SP4N Lapor, anti narkoba/bullying secara teratur."
        },
        {
            "event_group": "01_HARI_REGULER",
            "event_name": "Religi Reguler Sore",
            "time": "18:00:00",
            "command_type": "load",
            "target_path": os.path.join(playlist_dir, "1800_RELIGI_REGULER.m3u8"),
            "risk_level": "LOW",
            "status": "READY",
            "notes": "Lagu religi reguler non-Ramadhan menyambut malam hari."
        },
        {
            "event_group": "02_ADZAN_OTOMATIS",
            "event_name": "Adzan Maghrib Otomatis",
            "time": "18:08:00",
            "command_type": "play",
            "target_path": adzan_file,
            "risk_level": "LOW",
            "status": "READY",
            "notes": "Event pemutaran adzan Maghrib. Verifikasi jam setempat secara berkala."
        }
    ]
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'scheduler_plan')
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, 'radioboss_scheduler_plan.csv')
    
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["event_group", "event_name", "time", "command_type", "target_path", "risk_level", "status", "notes"])
            for item in new_plan:
                writer.writerow([
                    item["event_group"], item["event_name"], item["time"], item["command_type"],
                    item["target_path"], item["risk_level"], item["status"], item["notes"]
                ])
                
        # Salin juga ke folder fresh 08_RADIOBOSS_EXPORT stasiun radio
        fresh_export_dir = os.path.join(fresh_root, "08_RADIOBOSS_EXPORT")
        os.makedirs(fresh_export_dir, exist_ok=True)
        shutil_dest = os.path.join(fresh_export_dir, "radioboss_scheduler_plan.csv")
        
        # Lakukan copy manual (simulasi)
        with open(shutil_dest, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["event_group", "event_name", "time", "command_type", "target_path", "risk_level", "status", "notes"])
            for item in new_plan:
                writer.writerow([
                    item["event_group"], item["event_name"], item["time"], item["command_type"],
                    item["target_path"], item["risk_level"], item["status"], item["notes"]
                ])
                
    except Exception as e:
        print(f"Error saving scheduler plan: {e}")
        
    return len(new_plan)

if __name__ == "__main__":
    res = generate_scheduler_plan()
    print("Scheduler Plan Builder selesai. Berhasil membuat", res, "rencana event siaran.")
