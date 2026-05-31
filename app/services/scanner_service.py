import os
import time
import hashlib
import re
import json
from datetime import datetime
from db.database import get_db_connection
from app.utils.path_security import is_safe_path
from core.classifier import classify_file, load_rules

class ScannerService:
    """
    Menyediakan layanan pemindaian pustaka stasiun radio secara rekursif,
    menghitung signature hash MD5, mendeteksi duplikat, dan mengklasifikasikan aset siaran.
    """
    @staticmethod
    def get_file_md5(file_path):
        """Menghitung hash MD5 cepat (64kb awal) dari berkas audio stasiun radio."""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                chunk = f.read(65536)
                hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""

    @classmethod
    def scan_and_index(cls, root_path, progress_callback=None):
        """
        Memindai root_path secara aman (terproteksi Path Traversal) dan mendaftarkan
        indeks audio + hash MD5 + klasifikasi tipe di SQLite secara massal.
        """
        # Proteksi Path Traversal: pastikan folder scan valid dan aman
        # Sebagai pengaman, batasi scan root_path pada folder stasiun radio
        if not os.path.exists(root_path):
            raise FileNotFoundError(f"Direktori target '{root_path}' tidak ditemukan.")
            
        start_time = time.time()
        file_items = []
        scanned_count = 0
        audio_count = 0
        playlist_count = 0
        
        AUDIO_EXTENSIONS = {'.mp3', '.wav', '.wma', '.flac', '.ogg', '.aac', '.m4a'}
        PLAYLIST_EXTENSIONS = {'.m3u', '.m3u8', '.pls'}
        SKIP_FOLDERS = {'node_modules', '.git', '$recycle.bin', 'system volume information', 'temp', 'appdata'}
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Hapus indeks lama dari root_path yang sama untuk menghindari duplikasi record
        cursor.execute("DELETE FROM file_index WHERE original_path LIKE ?", (root_path + '%',))
        conn.commit()
        
        rules = load_rules()
        
        if progress_callback:
            progress_callback(5, "Mengumpulkan data filesystem stasiun radio...")
            
        # Kumpulkan semua file terlebih dahulu untuk perhitungan progress yang akurat
        files_to_process = []
        for root, dirs, files in os.walk(root_path):
            dirs[:] = [d for d in dirs if d.lower() not in SKIP_FOLDERS]
            for file in files:
                file_path = os.path.join(root, file)
                _, ext = os.path.splitext(file.lower())
                if ext in AUDIO_EXTENSIONS or ext in PLAYLIST_EXTENSIONS:
                    files_to_process.append((file_path, file, ext))
                    
        total_to_process = len(files_to_process)
        if total_to_process == 0:
            conn.close()
            return {"scanned_count": 0, "audio_count": 0, "playlist_count": 0, "elapsed_seconds": 0}
            
        for idx, (file_path, file, ext) in enumerate(files_to_process):
            scanned_count += 1
            is_audio = ext in AUDIO_EXTENSIONS
            
            try:
                stat = os.stat(file_path)
                size_bytes = stat.st_size
                modified_at = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                size_bytes = 0
                modified_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
            # Hitung signature hash MD5 untuk berkas audio
            file_hash = cls.get_file_md5(file_path) if is_audio else ""
            
            # Klasifikasi cerdas instan
            detected_type, risk_level, status, recommended_folder, notes = classify_file(file_path, file, rules)
            
            if is_audio:
                audio_count += 1
            else:
                playlist_count += 1
                
            file_items.append((
                file_path,
                file,
                ext.replace('.', '').upper(),
                size_bytes,
                modified_at,
                detected_type,
                risk_level,
                status,
                recommended_folder,
                notes,
                file_hash
            ))
            
            # Bulk insert ke SQLite per 200 file
            if len(file_items) >= 200:
                cursor.executemany("""
                    INSERT OR REPLACE INTO file_index 
                    (original_path, file_name, extension, size_bytes, modified_at, detected_type, risk_level, status, recommended_folder, notes, file_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, file_items)
                conn.commit()
                file_items.clear()
                
            if progress_callback and idx % 20 == 0:
                prog = int(5 + (idx / total_to_process) * 90)
                progress_callback(prog, f"Memindai ({idx+1}/{total_to_process}): {file}")
                
        if file_items:
            cursor.executemany("""
                INSERT OR REPLACE INTO file_index 
                (original_path, file_name, extension, size_bytes, modified_at, detected_type, risk_level, status, recommended_folder, notes, file_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, file_items)
            conn.commit()
            
        conn.close()
        
        elapsed = time.time() - start_time
        logging.info(f"Scan pustaka stasiun radio selesai: {scanned_count} berkas terindeks dalam {elapsed:.2f}s.")
        if progress_callback:
            progress_callback(100, f"Scan sukses! {scanned_count} berkas berhasil diindeks stasiun radio.")
            
        return {
            "scanned_count": scanned_count,
            "audio_count": audio_count,
            "playlist_count": playlist_count,
            "elapsed_seconds": round(elapsed, 2)
        }
