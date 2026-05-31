import os
import shutil
import zipfile
import logging
from datetime import datetime
from app.utils.path_security import is_safe_path

class BackupService:
    """
    Mengelola pencadangan (backup) otomatis aset penting stasiun radio (playlist lama)
    ke dalam berkas zip steril di bawah folder 00_ARSIP_LAMA.
    """
    @staticmethod
    def create_backup(source_dir, dest_root_fresh, progress_callback=None):
        """
        Mengompresi seluruh file playlist (.m3u, .m3u8, .pls) lama dari source_dir 
        ke dalam arsip ZIP di folder steril dest_root_fresh/00_ARSIP_LAMA.
        """
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Folder sumber backup '{source_dir}' tidak ditemukan.")
            
        backup_dest_dir = os.path.join(dest_root_fresh, "00_ARSIP_LAMA", "BACKUPS")
        os.makedirs(backup_dest_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_filename = f"Playlist_Backup_Sebelum_Reset_{timestamp}.zip"
        zip_path = os.path.join(backup_dest_dir, zip_filename)
        
        logging.info(f"Memulai backup otomatis dari {source_dir} ke {zip_path}")
        if progress_callback:
            progress_callback(10, "Mengumpulkan file playlist lama untuk backup...")
            
        playlist_extensions = {'.m3u', '.m3u8', '.pls'}
        files_to_zip = []
        
        # Cari berkas playlist lama secara rekursif
        for root, _, files in os.walk(source_dir):
            for file in files:
                _, ext = os.path.splitext(file.lower())
                if ext in playlist_extensions:
                    full_path = os.path.join(root, file)
                    files_to_zip.append(full_path)
                    
        if not files_to_zip:
            logging.info("Tidak ada file playlist yang ditemukan untuk dibackup.")
            if progress_callback:
                progress_callback(100, "Tidak ada file playlist yang ditemukan. Melanjutkan reset...")
            return None
            
        total_files = len(files_to_zip)
        
        # Buat kompresi ZIP
        try:
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for idx, file_path in enumerate(files_to_zip):
                    # Tulis path relatif di dalam ZIP agar tidak merekam absolut drive local
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
                    
                    if progress_callback:
                        prog = int(10 + (idx / total_files) * 80)
                        progress_callback(prog, f"Mencadangkan file ({idx+1}/{total_files}): {os.path.basename(file_path)}")
                        
            logging.info(f"Backup otomatis sukses dibuat: {zip_path}")
            if progress_callback:
                progress_callback(100, f"Backup zip sukses dibuat di: 00_ARSIP_LAMA/BACKUPS/{zip_filename}")
            return zip_path
        except Exception as e:
            logging.error(f"Gagal melakukan backup otomatis: {e}")
            raise e
