import os
import csv
import re
from db.database import get_db_connection

def analyze_scheduler_events(custom_events_list=None):
    """
    Menganalisis event scheduler RadioBOSS. Jika custom_events_list kosong,
    modul akan memuat event simulasi default berbasis kondisi nyata dari screenshot.
    Menyimpan hasil analisis ke database SQLite dan mengekspor laporan CSV.
    """
    events = custom_events_list
    
    # 1. Jika tidak ada input custom, gunakan simulasi event riil dari screenshot stasiun radio
    if not events:
        events = [
            {
                "event_group": "RAMADHAN 2026",
                "event_name": "Berbuka Puasa SBL",
                "time": "18:14:40",
                "command_type": "load",
                "target_path": "E:\\SUARA BUMI LASINRANG 2025\\RAMADHAN\\berbuka puasa.m3u8"
            },
            {
                "event_group": "RAMADHAN 2026",
                "event_name": "Tips Sahur 04:30",
                "time": "04:30:00",
                "command_type": "play",
                "target_path": "E:\\SUARA BUMI LASINRANG 2025\\RAMADHAN\\Tips Sahur SBL.mp3"
            },
            {
                "event_group": "SUBUH",
                "event_name": "Imsak 04:42",
                "time": "04:42:00",
                "command_type": "multiple",
                "target_path": "E:\\SUARA BUMI LASINRANG 2025\\RAMADHAN"
            },
            {
                "event_group": "JINGLE",
                "event_name": "Jingle Ramadhan Rotasi",
                "time": "03:00:00",
                "command_type": "load",
                "target_path": "JINGLE RAMADHAN ROTASI.m3u8"
            },
            {
                "event_group": "Pagi",
                "event_name": "Indo Pagi Rotasi",
                "time": "07:00:00",
                "command_type": "getrandomplaylist",
                "target_path": "E:\\agus lagu baru"
            },
            {
                "event_group": "ADZAN",
                "event_name": "ADZAN MAGHRIB",
                "time": "18:08:00",
                "command_type": "play",
                "target_path": "E:\\SUARA BUMI LASINRANG\\Adzan - Radio SBL.mp3"
            },
            {
                "event_group": "JINGLE",
                "event_name": "Station ID Jingle",
                "time": "12:00:00",
                "command_type": "play",
                "target_path": "E:\\SUARA BUMI LASINRANG\\Jingle SBL Reguler.mp3"
            },
            {
                "event_group": "Kultum",
                "event_name": "Hikmah Puasa Sore",
                "time": "17:45:00",
                "command_type": "play",
                "target_path": "E:\\SUARA BUMI LASINRANG 2025\\RAMADHAN\\Hikmah Puasa.mp3"
            }
        ]

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Bersihkan data lama
    cursor.execute("DELETE FROM scheduler_events")
    conn.commit()
    
    analyzed_items = []
    
    for ev in events:
        group = ev["event_group"]
        name = ev["event_name"]
        time_str = ev["time"]
        cmd_type = ev["command_type"]
        target = ev["target_path"]
        
        # Default klasifikasi
        risk_level = "LOW"
        status = "KEEP_ACTIVE"
        recommended_action = "Biarkan aktif untuk siaran reguler."
        notes = "OK"
        
        target_exists = 1 if os.path.exists(target) else 0
        if not target_exists and os.path.isabs(target):
            risk_level = "HIGH"
            status = "BROKEN_PATH"
            recommended_action = "Segera relink file ke master folder baru."
            notes = "Target file tidak ditemukan di disk fisik (Error Code 2)."
            
        group_lower = group.lower()
        name_lower = name.lower()
        target_lower = target.lower()
        
        # 1. Aturan Ramadhan/Seasonal Archive
        seasonal_keywords = ["ramadhan", "imsak", "sahur", "puasa", "berbuka", "buka puasa", "takbiran", "kultum", "tarawih"]
        is_seasonal = False
        for kw in seasonal_keywords:
            if kw in group_lower or kw in name_lower or kw in target_lower:
                is_seasonal = True
                break
                
        if is_seasonal:
            risk_level = "CRITICAL"
            status = "SEASONAL_RAMADHAN_ARCHIVE"
            recommended_action = "Disable outside Ramadhan / Move to seasonal archive."
            notes = "Materi Ramadhan aktif di luar bulan suci. Nonaktifkan segera."
            
        # 2. Aturan Adzan Event
        elif "adzan" in name_lower or "adzan" in group_lower or "adzan" in target_lower:
            risk_level = "MEDIUM"
            status = "ADZAN_REVIEW"
            recommended_action = "Validate time, target file, and local prayer schedule."
            notes = "Event pemutaran adzan wajib diverifikasi berkala agar cocok dengan jam shalat daerah."
            
        # 3. Aturan Random Source yang Berbahaya
        elif cmd_type == "getrandomplaylist" or "lagu baru" in target_lower or "campur" in target_lower or "download" in target_lower:
            risk_level = "HIGH"
            status = "DANGEROUS_RANDOM_SOURCE"
            recommended_action = "Replace source directory with Clean Master Category folder."
            notes = "Memanggil folder musik kotor secara acak. Sangat berisiko memicu playback crash."
            
        cursor.execute("""
            INSERT INTO scheduler_events
            (event_group, event_name, time, command_type, target_path, target_exists, risk_level, status, recommended_action, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (group, name, time_str, cmd_type, target, target_exists, risk_level, status, recommended_action, notes))
        
        analyzed_items.append({
            "event_group": group,
            "event_name": name,
            "time": time_str,
            "command_type": cmd_type,
            "target_path": target,
            "target_exists": target_exists == 1,
            "risk_level": risk_level,
            "status": status,
            "recommended_action": recommended_action,
            "notes": notes
        })
        
    conn.commit()
    conn.close()
    
    # 4. Ekspor laporan CSV ke output/reports/
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    # Laporan Emergency Scheduler
    csv_path = os.path.join(output_dir, 'scheduler_emergency_cleanup.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["event_group", "event_name", "time", "command_type", "target_path", "target_exists", "risk_level", "status", "recommended_action", "notes"])
        for item in analyzed_items:
            writer.writerow([
                item["event_group"], item["event_name"], item["time"], item["command_type"],
                item["target_path"], "TRUE" if item["target_exists"] else "FALSE",
                item["risk_level"], item["status"], item["recommended_action"], item["notes"]
            ])
            
    # Laporan Command Risk
    csv_risk_path = os.path.join(output_dir, 'scheduler_command_risk.csv')
    with open(csv_risk_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["event_name", "command_type", "target_path", "risk_level", "status", "recommended_action"])
        for item in analyzed_items:
            if item["risk_level"] in {"HIGH", "CRITICAL"}:
                writer.writerow([
                    item["event_name"], item["command_type"], item["target_path"],
                    item["risk_level"], item["status"], item["recommended_action"]
                ])
                
    return analyzed_items

if __name__ == "__main__":
    from db.database import init_db
    init_db()
    res = analyze_scheduler_events()
    print("Analisis scheduler selesai. Ditemukan", len(res), "event.")
