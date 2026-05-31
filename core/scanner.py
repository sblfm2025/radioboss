import os
import time
from datetime import datetime
from db.database import get_db_connection

# Ekstensi yang didukung untuk pencarian
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.wma', '.flac', '.ogg', '.aac', '.m4a'}
PLAYLIST_EXTENSIONS = {'.m3u', '.m3u8', '.pls'}

# Folder sistem/sensitif yang wajib dilewati
SKIP_FOLDERS = {
    'node_modules', '.git', '.github', '.vscode', '.idea',
    '$recycle.bin', 'system volume information', 'windows',
    'program files', 'program files (x86)', 'appdata', 'temp'
}

def scan_directory(root_path, progress_callback=None):
    """
    Memindai root_path secara rekursif untuk mencari berkas audio dan playlist.
    Menyimpan hasil pindai secara massal ke database file_index.
    """
    if not os.path.exists(root_path):
        raise FileNotFoundError(f"Folder '{root_path}' tidak ditemukan di disk.")
        
    start_time = time.time()
    file_items = []
    scanned_count = 0
    audio_count = 0
    playlist_count = 0
    
    # Koneksi ke database untuk menghapus indeks lama dari folder yang sama
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Hapus indeks lama yang berada di bawah folder root_path agar tidak terjadi duplikasi index
    cursor.execute("DELETE FROM file_index WHERE original_path LIKE ?", (root_path + '%',))
    conn.commit()

    for root, dirs, files in os.walk(root_path):
        # Memodifikasi dirs in-place untuk melompati folder sistem yang terdaftar di SKIP_FOLDERS
        dirs[:] = [d for d in dirs if d.lower() not in SKIP_FOLDERS]
        
        for file in files:
            scanned_count += 1
            file_path = os.path.join(root, file)
            _, ext = os.path.splitext(file.lower())
            
            is_audio = ext in AUDIO_EXTENSIONS
            is_playlist = ext in PLAYLIST_EXTENSIONS
            
            if is_audio or is_playlist:
                try:
                    stat = os.stat(file_path)
                    size_bytes = stat.st_size
                    modified_at = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                except Exception:
                    size_bytes = 0
                    modified_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                detected_type = "audio" if is_audio else "playlist"
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
                    "LOW",      # Risk level default
                    "APPROVED", # Status default
                    None,       # Recommended folder
                    None        # Notes
                ))
                
                # Simpan berkala setiap 500 file agar hemat memori
                if len(file_items) >= 500:
                    cursor.executemany("""
                        INSERT OR REPLACE INTO file_index 
                        (original_path, file_name, extension, size_bytes, modified_at, detected_type, risk_level, status, recommended_folder, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, file_items)
                    conn.commit()
                    file_items.clear()
                    
                if progress_callback:
                    progress_callback(scanned_count, audio_count, playlist_count, file_path)
                    
    # Simpan sisa berkas yang ada
    if len(file_items) > 0:
        cursor.executemany("""
            INSERT OR REPLACE INTO file_index 
            (original_path, file_name, extension, size_bytes, modified_at, detected_type, risk_level, status, recommended_folder, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, file_items)
        conn.commit()
        
    conn.close()
    
    elapsed = time.time() - start_time
    return {
        "scanned_count": scanned_count,
        "audio_count": audio_count,
        "playlist_count": playlist_count,
        "elapsed_seconds": round(elapsed, 2)
    }

if __name__ == "__main__":
    from db.database import init_db
    init_db()
    # Test scan folder lokal config
    current_dir = os.path.dirname(os.path.dirname(__file__))
    res = scan_directory(current_dir, lambda s, a, p, f: print(f"Scanned {s}... Audio: {a}, Playlists: {p}", end='\r'))
    print("\nScan selesai:", res)
