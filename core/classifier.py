import os
import json
import re
from db.database import get_db_connection

def load_rules():
    """Memuat aturan kata kunci klasifikasi dari keyword_rules.json."""
    config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
    rules_path = os.path.join(config_dir, 'keyword_rules.json')
    
    if os.path.exists(rules_path):
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading keyword_rules.json: {e}")
            
    # Fallback jika file config tidak dapat dibaca
    return {
        "categories": {
            "ramadhan_only": {
                "keywords": ["ramadhan", "imsak", "sahur", "buka puasa", "berbuka puasa", "tarawih", "takbiran", "kultum", "shalawat religi", "religi 2026", "puasa"],
                "recommended_folder": "05_ADZAN_DAN_MUSIMAN\\RAMADHAN_ONLY",
                "risk_level": "CRITICAL",
                "status": "SEASONAL_RAMADHAN_ARCHIVE",
                "notes": "Materi musiman Ramadhan. Nonaktifkan di luar bulan suci."
            },
            "adzan": {
                "keywords": ["adzan", "subuh", "dzuhur", "ashar", "maghrib", "isya"],
                "recommended_folder": "05_ADZAN_DAN_MUSIMAN\\ADZAN",
                "risk_level": "HIGH",
                "status": "ADZAN_REVIEW",
                "notes": "Validasi kecocokan jam lokal dan file target adzan."
            },
            "ilm_spot": {
                "keywords": ["spot", "iklan", "ilm", "narkoba", "bullying", "judi online", "judol", "lapor", "stop kekerasan", "layanan masyarakat"],
                "recommended_folder": "03_ILM",
                "risk_level": "MEDIUM",
                "status": "APPROVED",
                "notes": "Iklan Layanan Masyarakat atau Spot Siaran resmi."
            },
            "jingle_sweeper": {
                "keywords": ["jingle", "sweeper", "station id", "sbl id", "aga kareba", "sbl on stage", "salam subuh", "seputar pinrang"],
                "recommended_folder": "02_JINGLE_SWEEPER_ID",
                "risk_level": "LOW",
                "status": "APPROVED",
                "notes": "Jingle program stasiun atau station ID reguler."
            },
            "bed_music": {
                "keywords": ["instrumental", "bed", "latar", "saxophone", "bgm", "backsound", "piano"],
                "recommended_folder": "02_JINGLE_SWEEPER_ID",
                "risk_level": "LOW",
                "status": "APPROVED",
                "notes": "Musik instrumental latar penyiar (Bed Music)."
            }
        },
        "dirty_metadata": {
            "keywords": ["planetlagu", "stafaband", "gudang lagu", "download lagu", "mp3 juice", "tiktok version", "official music video", "youtube", "www.", "[www.", "lagu baru", "campur", "backup", "mentah"],
            "notes": "Mendeteksi label watermark download internet atau nama folder tidak rapi."
        }
    }

def classify_file(file_path, file_name, rules=None):
    """
    Menganalisis file_path dan file_name untuk mengklasifikasikan tipe file,
    tingkat risiko, status, recommended folder, dan catatan metadata kotor.
    """
    if rules is None:
        rules = load_rules()
        
    path_lower = file_path.lower()
    name_lower = file_name.lower()
    
    # 1. Inisialisasi nilai default (biasanya dianggap lagu musik reguler)
    detected_type = "music"
    risk_level = "LOW"
    status = "APPROVED"
    recommended_folder = "01_MUSIC_ACTIVE"
    notes = []
    
    # 2. Periksa apakah berkas merupakan file playlist
    _, ext = os.path.splitext(name_lower)
    if ext in {'.m3u', '.m3u8', '.pls'}:
        detected_type = "playlist"
        recommended_folder = "07_PLAYLIST_BARU"
        return detected_type, "LOW", "APPROVED", recommended_folder, "Berkas Playlist RadioBOSS"
        
    # 3. Klasifikasi Kategori Kritis Berdasarkan Kata Kunci
    matched_category = None
    
    # Prioritaskan pencocokan dari kategori kritis ke ringan
    category_priority = ["ramadhan_only", "adzan", "ilm_spot", "jingle_sweeper", "bed_music"]
    
    for cat_name in category_priority:
        cat_info = rules["categories"].get(cat_name)
        if not cat_info:
            continue
            
        for keyword in cat_info["keywords"]:
            # Cocokkan keyword dengan batas kata atau substring pada path/nama file
            pattern = re.compile(rf"\b{re.escape(keyword)}\b|{re.escape(keyword)}")
            if pattern.search(path_lower) or pattern.search(name_lower):
                matched_category = cat_name
                break
        if matched_category:
            break
            
    if matched_category:
        cat_info = rules["categories"][matched_category]
        detected_type = matched_category
        risk_level = cat_info["risk_level"]
        status = cat_info["status"]
        recommended_folder = cat_info["recommended_folder"]
        notes.append(cat_info["notes"])
        
    # 4. Deteksi Metadata Kotor (Watermark Unduhan/Watermark Website)
    dirty_rules = rules.get("dirty_metadata", {})
    is_dirty = False
    matched_dirty_keywords = []
    
    for keyword in dirty_rules.get("keywords", []):
        if keyword in path_lower or keyword in name_lower:
            is_dirty = True
            matched_dirty_keywords.append(keyword)
            
    if is_dirty:
        notes.append(f"DIRTY_METADATA: Mengandung kata unduhan/kotor '{', '.join(matched_dirty_keywords)}'. Perlu pembersihan tag/nama.")
        if status == "APPROVED":
            status = "REVIEW"  # Ubah ke REVIEW agar admin meninjau metadata
            
    notes_str = "; ".join(notes) if notes else "OK"
    return detected_type, risk_level, status, recommended_folder, notes_str

def run_classification_pipeline():
    """
    Mengambil semua data hasil scan dari SQLite, menerapkan logika klasifikasi,
    dan memperbarui tabel file_index secara massal.
    """
    rules = load_rules()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, original_path, file_name FROM file_index")
    rows = cursor.fetchall()
    
    updates = []
    for row in rows:
        file_id = row['id']
        path = row['original_path']
        name = row['file_name']
        
        detected_type, risk_level, status, recommended_folder, notes = classify_file(path, name, rules)
        
        updates.append((
            detected_type,
            risk_level,
            status,
            recommended_folder,
            notes,
            file_id
        ))
        
        # Eksekusi berkala setiap 500 baris
        if len(updates) >= 500:
            cursor.executemany("""
                UPDATE file_index
                SET detected_type = ?, risk_level = ?, status = ?, recommended_folder = ?, notes = ?
                WHERE id = ?
            """, updates)
            conn.commit()
            updates.clear()
            
    if len(updates) > 0:
        cursor.executemany("""
            UPDATE file_index
            SET detected_type = ?, risk_level = ?, status = ?, recommended_folder = ?, notes = ?
            WHERE id = ?
        """, updates)
        conn.commit()
        
    conn.close()
    return len(rows)

if __name__ == "__main__":
    # Test klasifikasi dummy
    rules = load_rules()
    print("Test Ramadhan:", classify_file("E:\\SUARA BUMI LASINRANG\\Tips Sahur 1.mp3", "Tips Sahur 1.mp3", rules))
    print("Test Adzan:", classify_file("E:\\SUARA BUMI LASINRANG\\Adzan Subuh.mp3", "Adzan Subuh.mp3", rules))
    print("Test Dirty Metadata:", classify_file("E:\\agus lagu baru\\Gudang Lagu - PlanetLagu.com - Kangen Band.mp3", "Kangen Band.mp3", rules))
    print("Test Reguler:", classify_file("E:\\agus lagu baru\\Peterpan - Bintang di Surga.mp3", "Bintang di Surga.mp3", rules))
