import os
import csv
from db.database import get_db_connection

def generate_cart_wall_plan(custom_cart_list=None):
    """
    Menyusun rencana pembagian ulang cart wall stasiun radio agar rapi.
    Menyimpan ke SQLite tabel cart_wall_items dan mengekspor laporan CSV.
    """
    items = custom_cart_list
    
    # Jika tidak ada custom_list, gunakan item simulasi dari screenshot riil stasiun radio SBL
    if not items:
        items = [
            {
                "current_tab": "SPOT",
                "slot": 1,
                "label": "SP4N LAPOR",
                "duration_seconds": 60.0,
                "current_path": "E:\\SUARA BUMI LASINRANG\\SP4N LAPOR ADUAN.mp3"
            },
            {
                "current_tab": "SPOT",
                "slot": 2,
                "label": "Stop Bullying",
                "duration_seconds": 45.0,
                "current_path": "E:\\SUARA BUMI LASINRANG\\Stop Bullying Anak.mp3"
            },
            {
                "current_tab": "SPOT",
                "slot": 3,
                "label": "Jauhi Narkoba",
                "duration_seconds": 30.0,
                "current_path": "E:\\SUARA BUMI LASINRANG\\Jauhi Narkoba SBL.mp3"
            },
            {
                "current_tab": "LATAR",
                "slot": 1,
                "label": "INSTRUMENTAL SAXOPHONE",
                "duration_seconds": 180.0,
                "current_path": "E:\\SUARA BUMI LASINRANG\\Instrumental Saxophone Background.mp3"
            },
            {
                "current_tab": "JINGLE",
                "slot": 1,
                "label": "Jingle SBL Ramadhan",
                "duration_seconds": 15.0,
                "current_path": "E:\\SUARA BUMI LASINRANG\\RAMADHAN\\Jingle SBL Ramadhan.mp3"
            },
            {
                "current_tab": "JINGLE",
                "slot": 2,
                "label": "Jingle OASE Ramadhan",
                "duration_seconds": 20.0,
                "current_path": "E:\\SUARA BUMI LASINRANG\\RAMADHAN\\Jingle OASE Ramadhan.mp3"
            },
            {
                "current_tab": "JINGLE",
                "slot": 3,
                "label": "Aga Kareba Program",
                "duration_seconds": 10.0,
                "current_path": "E:\\SUARA BUMI LASINRANG\\Jingle Program Aga Kareba.mp3"
            },
            {
                "current_tab": "JINGLE",
                "slot": 4,
                "label": "Salam Subuh Program",
                "duration_seconds": 12.0,
                "current_path": "E:\\SUARA BUMI LASINRANG\\Salam Subuh Intro.mp3"
            },
            {
                "current_tab": "JINGLE",
                "slot": 5,
                "label": "SBL Morning Song Reguler",
                "duration_seconds": 10.0,
                "current_path": "E:\\SUARA BUMI LASINRANG\\SBL Morning Song.mp3"
            }
        ]

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hapus data lama
    cursor.execute("DELETE FROM cart_wall_items")
    conn.commit()
    
    planned_items = []
    
    for item in items:
        cur_tab = item["current_tab"]
        slot = item["slot"]
        label = item["label"]
        duration = item["duration_seconds"]
        path = item["current_path"]
        
        # Tentukan detected type
        path_lower = path.lower()
        label_lower = label.lower()
        
        detected_type = "jingle_sweeper"
        new_tab = "TAB 3: SWEEPER"
        new_folder = "02_JINGLE_SWEEPER_ID"
        status = "APPROVED"
        notes = "Ditempatkan di tab Sweeper reguler."
        
        # Aturan Pemindahan:
        # 1. ILM / Spot Publik
        ilm_keywords = ["lapor", "bullying", "narkoba", "judi", "judol", "kekerasan", "stop", "iklan", "ilm"]
        is_ilm = False
        for kw in ilm_keywords:
            if kw in label_lower or kw in path_lower:
                is_ilm = True
                break
                
        if is_ilm:
            detected_type = "ilm_spot"
            new_tab = "TAB 4: ILM / SPOT PUBLIK"
            new_folder = "03_ILM"
            notes = "Dipindahkan ke Tab ILM/Spot Publik stasiun."
            
        # 2. Latar / Bed Music
        elif "instrumental" in label_lower or "latar" in label_lower or "saxophone" in label_lower or "bed" in label_lower or duration > 120:
            detected_type = "bed_music"
            new_tab = "TAB 5: LATAR / BED MUSIC"
            new_folder = "02_JINGLE_SWEEPER_ID"
            notes = "Dipindahkan ke Tab Bed Music/Latar pengisi siaran."
            
        # 3. Ramadhan Only
        elif "ramadhan" in label_lower or "ramadhan" in path_lower or "sahur" in label_lower or "imsak" in label_lower:
            detected_type = "ramadhan_only"
            new_tab = "TAB 8: RAMADHAN ONLY"
            new_folder = "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY"
            status = "ARCHIVE"
            notes = "Materi Ramadhan. Nonaktifkan di luar bulan Ramadhan."
            
        # 4. Jingle Program
        elif "program" in label_lower or "aga kareba" in label_lower or "subuh" in label_lower or "stage" in label_lower:
            detected_type = "jingle_program"
            new_tab = "TAB 2: JINGLE PROGRAM"
            new_folder = "02_JINGLE_SWEEPER_ID"
            notes = "Jingle Program Khusus Stasiun."
            
        # 5. Station ID
        elif "morning song" in label_lower or "night song" in label_lower or "sbl id" in label_lower or "reguler" in label_lower:
            detected_type = "station_id"
            new_tab = "TAB 1: STATION ID"
            new_folder = "02_JINGLE_SWEEPER_ID"
            notes = "Station ID Resmi Stasiun Radio SBL."
            
        cursor.execute("""
            INSERT INTO cart_wall_items
            (current_tab, slot, label, duration_seconds, current_path, detected_type, new_tab, new_folder, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cur_tab, slot, label, duration, path, detected_type, new_tab, new_folder, status, notes))
        
        planned_items.append({
            "current_tab": cur_tab,
            "slot": slot,
            "label": label,
            "duration_seconds": duration,
            "current_path": path,
            "detected_type": detected_type,
            "new_tab": new_tab,
            "new_folder": new_folder,
            "status": status,
            "notes": notes
        })
        
    conn.commit()
    conn.close()
    
    # Ekspor laporan CSV ke output/reports/
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, 'cart_wall_rebuild_plan.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["current_tab", "slot", "label", "duration_seconds", "current_path", "detected_type", "new_tab", "new_folder", "status", "notes"])
        for item in planned_items:
            writer.writerow([
                item["current_tab"], item["slot"], item["label"], item["duration_seconds"],
                item["current_path"], item["detected_type"], item["new_tab"], item["new_folder"],
                item["status"], item["notes"]
            ])
            
    return planned_items

if __name__ == "__main__":
    from db.database import init_db
    init_db()
    res = generate_cart_wall_plan()
    print("Rencana Cart Wall selesai dibuat. Ditemukan", len(res), "item.")
