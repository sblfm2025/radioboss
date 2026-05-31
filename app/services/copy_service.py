import os
import shutil
import csv
import hashlib
import time
import logging
from db.database import get_db_connection
from app.services.scanner_service import ScannerService
from core.fresh_folder_builder import load_fresh_root

class CopyService:
    """
    Mengelola pemindahan dan migrasi aset audio stasiun radio dengan prinsip Safe Copy:
    Hanya aksi COPY (menyalin) yang diizinkan; aksi Move dan Delete dinonaktifkan secara absolut.
    """
    @classmethod
    def migrate_approved_files(cls, progress_callback=None):
        """
        Menyalin berkas berstatus APPROVED ke fresh root target secara asinkron.
        Mengelola konflik nama, mencatat manifest copy, dan memperbarui database.
        """
        fresh_root = load_fresh_root()
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Ambil berkas APPROVED stasiun radio SBL
        cursor.execute("""
            SELECT id, original_path, file_name, detected_type, recommended_folder 
            FROM file_index 
            WHERE status = 'APPROVED' AND recommended_folder IS NOT NULL
        """)
        rows = cursor.fetchall()
        
        total_files = len(rows)
        if total_files == 0:
            conn.close()
            if progress_callback:
                progress_callback(100, "Tidak ada aset berstatus APPROVED yang perlu disalin.")
            return 0, 0
            
        logging.info(f"Memulai penyalinan fisik asinkron stasiun radio pada {total_files} file.")
        
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'reports')
        os.makedirs(output_dir, exist_ok=True)
        
        copy_manifest = []
        copy_conflicts = []
        
        copied_count = 0
        conflict_count = 0
        
        for idx, row in enumerate(rows):
            file_id = row['id']
            src_path = row['original_path']
            file_name = row['file_name']
            recommended_folder = row['recommended_folder']
            
            if progress_callback and idx % 5 == 0:
                prog = int(10 + (idx / total_files) * 80)
                progress_callback(prog, f"Menyalin ({idx+1}/{total_files}): {file_name}")
                
            dest_folder = os.path.join(fresh_root, recommended_folder)
            os.makedirs(dest_folder, exist_ok=True)
            
            dest_path = os.path.join(dest_folder, file_name)
            final_file_name = file_name
            is_conflict = False
            
            # Kelola konflik nama berkas
            if os.path.exists(dest_path):
                is_conflict = True
                conflict_count += 1
                
                src_size = os.path.getsize(src_path)
                dest_size = os.path.getsize(dest_path)
                
                if src_size == dest_size:
                    # File identik, abaikan copy (skip) stasiun radio
                    copy_manifest.append({
                        "src_path": src_path,
                        "dest_path": dest_path,
                        "status": "SKIPPED_IDENTICAL",
                        "notes": "Aset identik sudah tersedia di tujuan."
                    })
                    copied_count += 1
                    continue
                else:
                    # Rename dengan hash unik agar tidak menimpa berkas lama stasiun radio
                    file_base, ext = os.path.splitext(file_name)
                    short_hash = ScannerService.get_file_md5(src_path)[:8]
                    if not short_hash:
                        short_hash = str(int(time.time()))[-8:]
                    final_file_name = f"{file_base}_{short_hash}{ext}"
                    dest_path = os.path.join(dest_folder, final_file_name)
                    
                    copy_conflicts.append({
                        "original_name": file_name,
                        "new_name": final_file_name,
                        "dest_folder": recommended_folder,
                        "src_path": src_path,
                        "notes": "Aset berbeda memiliki nama sama. Rename otomatis dengan hash unik dilakukan."
                    })
                    
            # Aksi fisik COPY (Safe Copy)
            try:
                shutil.copy2(src_path, dest_path)
                status_str = "COPIED"
                if is_conflict:
                    status_str = "COPIED_WITH_RENAME"
                    
                copy_manifest.append({
                    "src_path": src_path,
                    "dest_path": dest_path,
                    "status": status_str,
                    "notes": f"Aset berhasil disalin ke {recommended_folder}."
                })
                
                # Update SQLite database path ke lokasi master steril stasiun radio yang baru
                cursor.execute("""
                    UPDATE file_index 
                    SET original_path = ?, file_name = ?, status = 'MIGRATED', notes = 'Aset berhasil dimigrasi ke folder steril.'
                    WHERE id = ?
                """, (dest_path, final_file_name, file_id))
                conn.commit()
            except Exception as e:
                logging.error(f"Gagal menyalin file {file_name}: {e}")
                copy_manifest.append({
                    "src_path": src_path,
                    "dest_path": dest_path,
                    "status": "FAILED",
                    "notes": f"Gagal menyalin: {e}"
                })
                
            copied_count += 1
            
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
                
        logging.info("Migrasi fisik Safe Copy stasiun radio selesai.")
        if progress_callback:
            progress_callback(100, f"Migrasi sukses! Berhasil menyalin {copied_count} berkas. Konflik diatasi: {conflict_count}")
            
        return copied_count, conflict_count
