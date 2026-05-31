import os
import logging
from db.database import get_db_connection
from core.playlist_parser import parse_playlist
from core.classifier import classify_file, load_rules

class PlaylistAuditService:
    """
    Mengelola audit playlist lama stasiun radio, melacak berkas hilang (Error Code 2),
    dan mengoperasikan Auto-Relink Engine cerdas untuk mencocokkan serta memperbaiki jalur secara otomatis.
    """
    @classmethod
    def audit_and_relink_playlists(cls, progress_callback=None):
        """
        Mengaudit seluruh playlist lama stasiun radio dari SQLite database,
        mencocokkan file-file yang hilang dengan folder master library steril yang baru,
        dan menuliskan kesimpulan audit beserta rincian item ke database.
        """
        rules = load_rules()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Ambil seluruh file playlist dari indeks scan stasiun radio
        cursor.execute("SELECT original_path, file_name FROM file_index WHERE detected_type = 'playlist'")
        playlist_rows = cursor.fetchall()
        
        # Bersihkan tabel audit lama
        cursor.execute("DELETE FROM playlist_audit")
        cursor.execute("DELETE FROM playlist_items")
        conn.commit()
        
        total_playlists = len(playlist_rows)
        if total_playlists == 0:
            conn.close()
            return 0
            
        logging.info(f"Memulai audit playlist + Auto-Relink pada {total_playlists} playlist.")
        
        for idx, row in enumerate(playlist_rows):
            playlist_path = row['original_path']
            playlist_name = row['file_name']
            
            if progress_callback:
                prog = int(10 + (idx / total_playlists) * 80)
                progress_callback(prog, f"Mengaudit playlist ({idx+1}/{total_playlists}): {playlist_name}")
                
            # Urai playlist lama stasiun radio
            items = parse_playlist(playlist_path)
            
            total_items = len(items)
            missing_items = 0
            dangerous_items = 0
            relinked_count = 0
            
            db_items_to_insert = []
            
            for item in items:
                raw_line = item["raw_line"]
                resolved_path = item["resolved_path"]
                exists = 1 if item["exists"] else 0
                item_name = os.path.basename(resolved_path)
                
                # Default klasifikasi berkas
                dtype, risk, status, rec_folder, notes = classify_file(resolved_path, item_name, rules)
                
                # --- AUTO-RELINK ENGINE ---
                # Jika file hilang (exists = 0), coba cari kecocokan di database SQLite master steril baru
                if not item["exists"]:
                    cursor.execute("""
                        SELECT original_path 
                        FROM file_index 
                        WHERE file_name = ? AND status IN ('APPROVED', 'MIGRATED')
                        LIMIT 1
                    """, (item_name,))
                    match = cursor.fetchone()
                    
                    if match:
                        # Sukses mencocokkan! Relink jalur otomatis stasiun radio SBL
                        resolved_path = match['original_path']
                        exists = 1  # Tandai sebagai beres (exists = 1)
                        relinked_count += 1
                        notes = f"AUTO_RELINK_SUCCESS: Jalur diperbaiki otomatis ke master steril baru."
                        status = "APPROVED"
                        risk = "LOW"
                    else:
                        missing_items += 1
                        notes = "MISSING_FILE: Berkas hilang di disk (Error Code 2). Perlu diisi manual."
                        status = "REVIEW"
                        risk = "HIGH"
                        
                is_dangerous = (status in {"SEASONAL_RAMADHAN_ARCHIVE", "ADZAN_REVIEW"} or "DIRTY_METADATA" in notes)
                if is_dangerous:
                    dangerous_items += 1
                    
                db_items_to_insert.append((
                    playlist_path,
                    raw_line,
                    resolved_path,
                    exists,
                    dtype,
                    risk,
                    status,
                    notes
                ))
                
            # Tentukan status akhir playlist
            if total_items == 0:
                status_pl = "EMPTY"
                rec_pl = "Playlist kosong atau tidak terbaca."
            elif missing_items == total_items:
                status_pl = "BROKEN"
                rec_pl = "CRITICAL: Semua file target hilang! Buat ulang playlist baru stasiun radio."
            elif missing_items > 0:
                status_pl = "NEEDS_RELINK"
                rec_pl = f"WARNING: Ada {missing_items} file hilang. Auto-relinked {relinked_count} file."
            elif dangerous_items > 0:
                status_pl = "DANGEROUS"
                rec_pl = f"REVIEW: Mengandung materi Ramadhan/adzan/kotor. Disarankan pemisahan."
            else:
                status_pl = "OK"
                rec_pl = "Aman digunakan untuk siaran reguler stasiun radio."
                
            # Simpan kesimpulan audit playlist ke SQLite
            cursor.execute("""
                INSERT INTO playlist_audit 
                (playlist_path, playlist_name, total_items, missing_items, dangerous_items, status, recommendation)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (playlist_path, playlist_name, total_items, missing_items, dangerous_items, status_pl, rec_pl))
            
            # Simpan rincian item dalam playlist ke SQLite
            if db_items_to_insert:
                cursor.executemany("""
                    INSERT INTO playlist_items
                    (playlist_path, item_path, resolved_path, file_exists, detected_type, risk_level, status, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, db_items_to_insert)
                
            conn.commit()
            
        conn.close()
        logging.info(f"Audit dan Auto-Relink playlist stasiun radio selesai diproses.")
        if progress_callback:
            progress_callback(100, f"Audit playlist sukses! Berhasil memetakan {total_playlists} playlist.")
            
        return total_playlists
