import os

def is_safe_path(path_to_check, allowed_root):
    """
    Memeriksa apakah path_to_check berada di dalam allowed_root secara aman.
    Menggunakan os.path.realpath untuk memecahkan symlink dan relative path traversal.
    """
    if not path_to_check:
        return False
        
    try:
        # Dapatkan real path absolut yang steril
        real_allowed = os.path.realpath(allowed_root)
        real_check = os.path.realpath(path_to_check)
        
        # Cek apakah check path diawali dengan allowed root path
        # Tambahkan trailing separator agar folder bertetangga seperti D:/RADIO_SBL_FRESH_kotor tidak lolos
        common_prefix = os.path.commonpath([real_allowed, real_check])
        return os.path.normpath(common_prefix) == os.path.normpath(real_allowed)
    except Exception:
        return False

def safe_join(base_dir, *paths):
    """
    Menggabungkan base_dir dengan sub-paths secara aman.
    Menghindari Path Traversal (seperti ../../../Windows).
    """
    joined = os.path.join(base_dir, *paths)
    if is_safe_path(joined, base_dir):
        return os.path.abspath(joined)
    else:
        raise PermissionError(f"Akses Keamanan Ditolak: Jalur '{joined}' terdeteksi di luar area aman '{base_dir}'.")
