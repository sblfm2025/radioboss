import os
from db.database import get_db_connection
from core.playlist_parser import parse_playlist
from core.classifier import classify_file, load_rules

def audit_all_playlists():
    """
    Mengambil seluruh file playlist dari database, mengaudit isi berkasnya secara mendalam,
    serta menyimpan kesimpulan audit dan rincian item ke database SQLite.
    """
    rules = load_rules()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Ambil daftar playlist dari indeks file scan
    cursor.execute("SELECT original_path, file_name FROM file_index WHERE detected_type = 'playlist'")
    playlist_rows = cursor.fetchall()
    
    # Bersihkan tabel audit lama sebelum melakukan audit baru agar data selalu segar
    cursor.execute("DELETE FROM playlist_audit")
    cursor.execute("DELETE FROM playlist_items")
    conn.commit()
    
    audited_count = 0
    
    for row in playlist_rows:
        playlist_path = row['original_path']
        playlist_name = row['file_name']
        
        # 2. Urai playlist untuk mendapatkan rincian item audio di dalamnya
        items = parse_playlist(playlist_path)
        
        total_items = len(items)
        missing_items = 0
        dangerous_items = 0
        
        db_items_to_insert = []
        
        for item in items:
            raw_line = item["raw_line"]
            resolved_path = item["resolved_path"]
            exists = 1 if item["exists"] else 0
            
            if not item["exists"]:
                missing_items += 1
                
            # Dapatkan klasifikasi risiko per file audio dalam playlist
            item_name = os.path.basename(resolved_path)
            detected_type, risk_level, status, recommended_folder, notes = classify_file(resolved_path, item_name, rules)
            
            # Tandai sebagai item berbahaya jika status diblokir reguler atau seasonal di luar bulan Ramadhan
            is_dangerous = (status in {"SEASONAL_RAMADHAN_ARCHIVE", "ADZAN_REVIEW"} or "DIRTY_METADATA" in notes)
            if is_dangerous:
                dangerous_items += 1
                
            db_items_to_insert.append((
                playlist_path,
                raw_line,
                resolved_path,
                exists,
                detected_type,
                risk_level,
                status,
                notes
            ))
            
        # Tentukan status akhir dan rekomendasi untuk playlist
        if total_items == 0:
            status = "EMPTY"
            recommendation = "Playlist kosong atau tidak terbaca."
        elif missing_items == total_items:
            status = "BROKEN"
            recommendation = "CRITICAL: Semua file target hilang! Buat ulang playlist baru."
        elif missing_items > 0:
            status = "NEEDS_RELINK"
            recommendation = f"WARNING: Ada {missing_items} file hilang. Jalankan Relink ke Master Library."
        elif dangerous_items > 0:
            status = "DANGEROUS"
            recommendation = f"REVIEW: Mengandung materi seasonal Ramadhan/adzan/kotor. Disarankan pemisahan."
        else:
            status = "OK"
            recommendation = "Aman digunakan untuk siaran reguler stasiun radio."
            
        # Simpan kesimpulan audit playlist ke SQLite
        cursor.execute("""
            INSERT INTO playlist_audit 
            (playlist_path, playlist_name, total_items, missing_items, dangerous_items, status, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (playlist_path, playlist_name, total_items, missing_items, dangerous_items, status, recommendation))
        
        # Simpan rincian item dalam playlist ke SQLite
        if db_items_to_insert:
            cursor.executemany("""
                INSERT INTO playlist_items
                (playlist_path, item_path, resolved_path, file_exists, detected_type, risk_level, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, db_items_to_insert)
            
        conn.commit()
        audited_count += 1
        
    conn.close()
    return audited_count

if __name__ == "__main__":
    # Test audit playlist
    res = audit_all_playlists()
    print(f"Audit selesai. Berhasil mengaudit {res} file playlist.")
