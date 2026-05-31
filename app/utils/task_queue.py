import uuid
import queue
import threading
import logging
import time

class TaskQueueManager:
    """
    Mengelola antrean tugas (task queue) latar belakang secara asinkron
    menggunakan background thread tunggal untuk menjamin eksekusi FIFO yang aman.
    """
    def __init__(self):
        self.task_queue = queue.Queue()
        self.tasks_status = {}
        self.lock = threading.Lock()
        
        # Mulai thread worker latar belakang
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        logging.info("Task Queue Background Worker Thread dimulai.")

    def add_task(self, name, target_fn, *args, **kwargs):
        """Menambahkan tugas baru ke dalam antrean dan mengembalikan task_id unik."""
        task_id = str(uuid.uuid4())
        
        with self.lock:
            self.tasks_status[task_id] = {
                "id": task_id,
                "name": name,
                "status": "PENDING",
                "progress": 0,
                "message": "Menunggu giliran antrean siaran...",
                "result": None,
                "created_at": time.time()
            }
            
        self.task_queue.put((task_id, target_fn, args, kwargs))
        return task_id

    def get_status(self, task_id):
        """Mengambil status detail kemajuan dari tugas berdasarkan task_id."""
        with self.lock:
            return self.tasks_status.get(task_id)

    def update_progress(self, task_id, progress, message=None):
        """Memperbarui persentase progress dan pesan secara thread-safe dari worker."""
        with self.lock:
            if task_id in self.tasks_status:
                self.tasks_status[task_id]["progress"] = progress
                if message:
                    self.tasks_status[task_id]["message"] = message

    def _worker_loop(self):
        """Loop utama background thread yang mengambil tugas dan mengeksekusinya."""
        while True:
            try:
                # Blokir thread sampai tugas masuk antrean
                task_id, target_fn, args, kwargs = self.task_queue.get()
                
                with self.lock:
                    if task_id in self.tasks_status:
                        self.tasks_status[task_id]["status"] = "RUNNING"
                        self.tasks_status[task_id]["message"] = "Tugas sedang diproses..."
                
                # Masukkan callback update progress otomatis jika fungsi target menerimanya
                kwargs['progress_callback'] = lambda prog, msg: self.update_progress(task_id, prog, msg)
                
                try:
                    # Jalankan fungsi tugas bisnis
                    result = target_fn(*args, **kwargs)
                    
                    with self.lock:
                        self.tasks_status[task_id]["status"] = "SUCCESS"
                        self.tasks_status[task_id]["progress"] = 100
                        self.tasks_status[task_id]["message"] = "Tugas berhasil diselesaikan!"
                        self.tasks_status[task_id]["result"] = result
                except Exception as e:
                    logging.error(f"Error executing task {task_id}: {e}", exc_info=True)
                    with self.lock:
                        self.tasks_status[task_id]["status"] = "FAILED"
                        self.tasks_status[task_id]["message"] = f"Gagal mengeksekusi tugas: {str(e)}"
                finally:
                    self.task_queue.task_done()
            except Exception as e:
                logging.error(f"Fatal error in task queue worker loop: {e}")
                time.sleep(1) # Delay recovery jika terjadi fatal error
