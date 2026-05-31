import os
import shutil
import csv
import hashlib
import time
from db.database import get_db_connection
from core.fresh_folder_builder import load_fresh_root

def generate_file_hash(file_path):
    """Menghasilkan hash MD5 pendek (8 karakter) untuk menangani konflik nama file."""
    try:
        hasher = hashlib.md5()
        # Baca 64kb pertama untuk kecepatan dibanding membaca seluruh file besar
        with open(file_path, 'rb') as f:
            chunk = f.read(65536)
            hasher.update(chunk)
        return hasher.hexdigest()[:8]
    except Exception:
        return str(int(time.time()))[-8:]

def copy_approved_files(progress_callback=None):
    """
    Menyalin seluruh file audio berstatus APPROVED dari folder lama ke folder target fresh root.
    Menghindari overwrite file, mengelola konflik nama, dan mengekspor laporan CSV.
    """
    fresh_root = load_fresh_root()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ambil file yang bertipe APPROVED
    cursor.execute("""
        SELECT id, original_path, file_name, detected_type, recommended_folder 
        FROM file_index 
        WHERE status = 'APPROVED' AND recommended_folder IS NOT NULL
    """)
    rows = cursor.fetchall()
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    copy_manifest = []
    copy_conflicts = []
    
    total_files = len(rows)
    copied_count = 0
    conflict_count = 0
    
    for row in rows:
        file_id = row['id']
        src_path = row['original_path']
        file_name = row['file_name']
        recommended_folder = row['recommended_folder']
        
        dest_folder = os.path.join(fresh_root, recommended_folder)
        os.makedirs(dest_folder, exist_ok=True)
        
        dest_path = os.path.join(dest_folder, file_name)
        final_file_name = file_name
        is_conflict = False
        
        # Cek jika terjadi konflik nama file
        if os.path.exists(dest_path):
            is_conflict = True
            conflict_count += 1
            
            # Bandingkan apakah file identik (ukuran sama)
            src_size = os.path.getsize(src_path)
            dest_size = os.path.getsize(dest_path)
            
            if src_size == dest_size:
                # File identik, abaikan copy (skip) demi menghemat storage stasiun radio
                copy_manifest.append({
                    "src_path": src_path,
                    "dest_path": dest_path,
                    "status": "SKIPPED_IDENTICAL",
                    "notes": "File dengan nama dan ukuran sama sudah ada di folder tujuan."
                })
                copied_count += 1
                if progress_callback:
                    progress_callback(copied_count, total_files, src_path, "SKIPPED")
                continue
            else:
                # Berbeda isi tapi nama sama, rename dengan menyisipkan hash unik
                file_base, ext = os.path.splitext(file_name)
                short_hash = generate_file_hash(src_path)
                final_file_name = f"{file_base}_{short_hash}{ext}"
                dest_path = os.path.join(dest_folder, final_file_name)
                
                copy_conflicts.append({
                    "original_name": file_name,
                    "new_name": final_file_name,
                    "dest_folder": recommended_folder,
                    "src_path": src_path,
                    "notes": "Konflik nama terdeteksi. Berkas di-rename otomatis dengan hash unik."
                })
                
        # Lakukan aksi fisik COPY aman (bukan move)
        try:
            shutil.copy2(src_path, dest_path)
            status_str = "COPIED"
            if is_conflict:
                status_str = "COPIED_WITH_RENAME"
                
            copy_manifest.append({
                "src_path": src_path,
                "dest_path": dest_path,
                "status": status_str,
                "notes": f"Berhasil disalin ke {recommended_folder}."
            })
            
            # Update database path agar mengarah ke master folder yang baru
            cursor.execute("""
                UPDATE file_index 
                SET original_path = ?, file_name = ?, status = 'MIGRATED', notes = 'File berhasil dimigrasi ke folder steril.'
                WHERE id = ?
            """, (dest_path, final_file_name, file_id))
            conn.commit()
            
        except Exception as e:
            copy_manifest.append({
                "src_path": src_path,
                "dest_path": dest_path,
                "status": "FAILED",
                "notes": f"Gagal menyalin file: {e}"
            })
            
        copied_count += 1
        if progress_callback:
            progress_callback(copied_count, total_files, src_path, "COPIED")
            
    conn.close()
    
    # Ekspor laporan copy_manifest.csv
    with open(os.path.join(output_dir, 'copy_manifest.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["src_path", "dest_path", "status", "notes"])
        for item in copy_manifest:
            writer.writerow([item["src_path"], item["dest_path"], item["status"], item["notes"]])
            
    # Ekspor laporan copy_conflicts.csv
    with open(os.path.join(output_dir, 'copy_conflicts.csv'), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["original_name", "new_name", "dest_folder", "src_path", "notes"])
        for item in copy_conflicts:
            writer.writerow([item["original_name"], item["new_name"], item["dest_folder"], item["src_path"], item["notes"]])
            
    return total_files, conflict_count

if __name__ == "__main__":
    from db.database import init_db
    init_db()
    # Test copy approved
    print("Memulai penyalinan...")
    res = copy_approved_files(lambda c, t, p, s: print(f"Copying {c}/{t}: {os.path.basename(p)} - {s}"))
    print("\nPenyalinan selesai. Total file:", res[0], "Konflik:", res[1])
