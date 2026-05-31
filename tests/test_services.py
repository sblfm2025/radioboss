import os
import unittest
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.scanner_service import ScannerService
from app.utils.task_queue import TaskQueueManager

class TestServices(unittest.TestCase):
    def test_file_md5_hashing(self):
        # Buat berkas dummy sementara
        dummy_file = "test_dummy_hash.mp3"
        with open(dummy_file, 'w') as f:
            f.write("Aset dummy audio stasiun radio SBL.")
            
        try:
            # Hitung hash
            file_hash = ScannerService.get_file_md5(dummy_file)
            self.assertEqual(len(file_hash), 32)  # Panjang MD5 hex adalah 32 karakter
        finally:
            if os.path.exists(dummy_file):
                os.remove(dummy_file)

    def test_task_queue_async_worker(self):
        # Tes antrean tugas asinkron (non-blocking)
        manager = TaskQueueManager()
        
        def dummy_heavy_job(progress_callback=None):
            if progress_callback:
                progress_callback(50, "Separuh jalan...")
            time.sleep(0.1)
            return "SUCCESS_DATA"
            
        task_id = manager.add_task("Uji Coba Latar Belakang", dummy_heavy_job)
        
        # Cek status penambahan awal
        status = manager.get_status(task_id)
        self.assertEqual(status["status"], "PENDING")
        
        # Tunggu eksekusi thread latar belakang selesai
        time.sleep(0.3)
        
        status_after = manager.get_status(task_id)
        self.assertEqual(status_after["status"], "SUCCESS")
        self.assertEqual(status_after["progress"], 100)
        self.assertEqual(status_after["result"], "SUCCESS_DATA")

if __name__ == "__main__":
    unittest.main()
