import os
import re

def parse_m3u(playlist_path):
    """
    Mengurai playlist berformat M3U/M3U8.
    Mengembalikan daftar item dengan absolut path yang di-resolve.
    """
    items = []
    playlist_dir = os.path.dirname(playlist_path)
    
    # Coba berbagai encoding populer agar tidak crash
    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
    lines = []
    
    for encoding in encodings:
        try:
            with open(playlist_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break  # Berhasil membaca file, hentikan coba encoding
        except (UnicodeDecodeError, LookupError):
            continue
            
    if not lines:
        return items  # Mengembalikan list kosong jika file gagal dibaca
        
    for line in lines:
        line = line.strip()
        
        # Lewati komentar M3U (#EXTM3U, #EXTINF, dll.) atau baris kosong
        if not line or line.startswith('#'):
            continue
            
        # Bersihkan karakter aneh di Windows path
        line = line.replace('"', '').replace("'", "")
        
        # Resolve relative path ke absolut path berdasarkan posisi file playlist
        if not os.path.isabs(line):
            resolved_path = os.path.abspath(os.path.join(playlist_dir, line))
        else:
            resolved_path = os.path.abspath(line)
            
        exists = os.path.exists(resolved_path)
        _, ext = os.path.splitext(resolved_path)
        
        items.append({
            "raw_line": line,
            "resolved_path": resolved_path,
            "exists": exists,
            "extension": ext.replace('.', '').upper()
        })
        
    return items

def parse_pls(playlist_path):
    """
    Mengurai playlist berformat PLS (format INI style).
    Mengembalikan daftar item dengan absolut path yang di-resolve.
    """
    items = []
    playlist_dir = os.path.dirname(playlist_path)
    
    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []
    
    for encoding in encodings:
        try:
            with open(playlist_path, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break
        except (UnicodeDecodeError, LookupError):
            continue
            
    if not lines:
        return items
        
    # Pola regex untuk mendeteksi baris berkas seperti: File1=E:\lagu\A.mp3
    file_pattern = re.compile(r'^file(\d+)\s*=\s*(.+)$', re.IGNORECASE)
    
    for line in lines:
        line = line.strip()
        match = file_pattern.match(line)
        
        if match:
            raw_path = match.group(2).strip()
            raw_path = raw_path.replace('"', '').replace("'", "")
            
            if not os.path.isabs(raw_path):
                resolved_path = os.path.abspath(os.path.join(playlist_dir, raw_path))
            else:
                resolved_path = os.path.abspath(raw_path)
                
            exists = os.path.exists(resolved_path)
            _, ext = os.path.splitext(resolved_path)
            
            items.append({
                "raw_line": raw_path,
                "resolved_path": resolved_path,
                "exists": exists,
                "extension": ext.replace('.', '').upper()
            })
            
    return items

def parse_playlist(playlist_path):
    """
    Wrapper umum untuk mendeteksi tipe playlist dan memanggil parser yang tepat.
    """
    _, ext = os.path.splitext(playlist_path.lower())
    if ext in {'.m3u', '.m3u8'}:
        return parse_m3u(playlist_path)
    elif ext == '.pls':
        return parse_pls(playlist_path)
    else:
        return []
