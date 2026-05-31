import os
import json
import logging
from flask import Flask, jsonify, render_template, request

# Impor wrapper database dan modul core Python
from db.database import init_db, get_db_connection, clear_all_tables
from core.scanner import scan_directory
from core.classifier import run_classification_pipeline, load_rules
from core.playlist_auditor import audit_all_playlists
from core.scheduler_emergency_analyzer import analyze_scheduler_events
from core.cart_wall_planner import generate_cart_wall_plan
from core.fresh_folder_builder import build_fresh_structure, load_fresh_root
from core.copy_manager import copy_approved_files
from core.m3u8_generator import generate_fresh_playlists
from core.scheduler_plan_builder import generate_scheduler_plan
from core.report_writer import generate_all_reports

# Inisialisasi aplikasi Flask dengan template & asset folder khusus
app = Flask(__name__, template_folder='ui/templates', static_folder='ui/static')

# Konfigurasi logging sistem stasiun radio
log_dir = os.path.join(os.path.dirname(__file__), 'output', 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

@app.route('/')
def home():
    """Halaman Dashboard Utama Web UI stasiun radio."""
    return render_template('index.html')

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Mengambil metrik statistik ringkas untuk widget dashboard utama stasiun radio."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    stats = {
        "total_files": 0,
        "music_files": 0,
        "playlist_files": 0,
        "ramadhan_files": 0,
        "adzan_files": 0,
        "dirty_metadata_files": 0,
        "broken_playlists": 0,
        "missing_paths": 0,
        "emergency_scheduler_count": 0,
        "fresh_root": load_fresh_root(),
        "readiness_status": "NOT_READY"
    }
    
    try:
        # Total Berkas
        cursor.execute("SELECT COUNT(*) FROM file_index")
        stats["total_files"] = cursor.fetchone()[0]
        
        # Total Lagu Reguler
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE detected_type = 'music'")
        stats["music_files"] = cursor.fetchone()[0]
        
        # Total Playlist
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE detected_type = 'playlist'")
        stats["playlist_files"] = cursor.fetchone()[0]
        
        # Total Ramadhan detected
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE detected_type = 'ramadhan_only'")
        stats["ramadhan_files"] = cursor.fetchone()[0]
        
        # Total Adzan detected
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE detected_type = 'adzan'")
        stats["adzan_files"] = cursor.fetchone()[0]
        
        # Total Dirty Metadata detected
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE notes LIKE '%DIRTY_METADATA%'")
        stats["dirty_metadata_files"] = cursor.fetchone()[0]
        
        # Total Playlist Rusak
        cursor.execute("SELECT COUNT(*) FROM playlist_audit WHERE status = 'BROKEN' OR status = 'NEEDS_RELINK'")
        stats["broken_playlists"] = cursor.fetchone()[0]
        
        # Total Missing path file audio
        cursor.execute("SELECT COUNT(*) FROM playlist_items WHERE file_exists = 0")
        stats["missing_paths"] = cursor.fetchone()[0]
        
        # Total Emergency scheduler
        cursor.execute("SELECT COUNT(*) FROM scheduler_events WHERE risk_level IN ('HIGH', 'CRITICAL')")
        stats["emergency_scheduler_count"] = cursor.fetchone()[0]
        
        # Tentukan status kesiapan reset stasiun
        if stats["total_files"] > 0 and stats["broken_playlists"] == 0 and stats["missing_paths"] == 0:
            stats["readiness_status"] = "READY"
            
    except Exception as e:
        logging.error(f"Gagal mengambil stats dashboard: {e}")
        
    conn.close()
    return jsonify(stats)

@app.route('/api/scan', methods=['POST'])
def run_scan():
    """Memicu pemindaian direktori filesystem secara realtime."""
    data = request.json or {}
    scan_folder = data.get("folder")
    
    if not scan_folder:
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'app_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                scan_folder = json.load(f).get("defaultScanFolder", "D:\\RADIO_MUSIC_INPUT_DEMO")
                
    if not os.path.exists(scan_folder):
        return jsonify({"status": "ERROR", "message": f"Folder input '{scan_folder}' tidak ditemukan di disk."}), 400
        
    try:
        logging.info(f"Memulai scan folder: {scan_folder}")
        res = scan_directory(scan_folder)
        
        # Otomatis jalankan klasifikasi & audit setelah scan selesai agar data instan dimuat
        run_classification_pipeline()
        audit_all_playlists()
        analyze_scheduler_events()
        generate_cart_wall_plan()
        
        logging.info("Scan, klasifikasi, dan audit playlist otomatis berhasil diselesaikan.")
        return jsonify({"status": "SUCCESS", "data": res})
    except Exception as e:
        logging.error(f"Gagal saat eksekusi scan: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/build-structure', methods=['POST'])
def build_structure():
    """Memicu pembangunan folder steril baru stasiun radio."""
    try:
        fresh_root, count = build_fresh_structure()
        logging.info(f"Struktur folder fresh sukses dibangun di {fresh_root}. Total {count} subfolder.")
        return jsonify({"status": "SUCCESS", "fresh_root": fresh_root, "created_folders": count})
    except Exception as e:
        logging.error(f"Gagal membuat struktur folder: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/copy-files', methods=['POST'])
def copy_files():
    """Memicu penyalinan fisik berkas APPROVED ke folder steril."""
    try:
        total, conflicts = copy_approved_files()
        logging.info(f"Penyalinan berkas selesai. Berhasil menyalin {total} file. Konflik nama: {conflicts}")
        return jsonify({"status": "SUCCESS", "total_copied": total, "conflicts": conflicts})
    except Exception as e:
        logging.error(f"Gagal saat proses salin file: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/generate-playlists', methods=['POST'])
def build_playlists():
    """Memicu penyusunan file playlist baru .m3u8 stasiun radio."""
    try:
        count = generate_fresh_playlists()
        logging.info(f"Playlist Builder selesai. Berhasil membuat {count} file .m3u8 reguler steril.")
        return jsonify({"status": "SUCCESS", "created_playlists": count})
    except Exception as e:
        logging.error(f"Gagal menyusun playlist: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/generate-scheduler-plan', methods=['POST'])
def build_scheduler_plan():
    """Memicu pembuatan rencana event scheduler yang baru."""
    try:
        count = generate_scheduler_plan()
        logging.info(f"Scheduler Plan selesai disusun. Terbuat {count} event steril baru.")
        return jsonify({"status": "SUCCESS", "events_created": count})
    except Exception as e:
        logging.error(f"Gagal membuat scheduler plan: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/generate-reports', methods=['POST'])
def build_reports():
    """Memicu ekspor seluruh laporan CSV/MD stasiun radio."""
    try:
        res = generate_all_reports()
        logging.info("Laporan CSV & MD berhasil diekspor secara menyeluruh.")
        return jsonify({"status": "SUCCESS", "reports_status": res})
    except Exception as e:
        logging.error(f"Gagal mengekspor laporan: {e}")
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/reset-data', methods=['POST'])
def reset_db_data():
    """Mereset seluruh tabel database stasiun radio."""
    try:
        clear_all_tables()
        logging.info("Tabel SQLite berhasil dikosongkan.")
        return jsonify({"status": "SUCCESS", "message": "Database berhasil dibersihkan."})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/scheduler-list', methods=['GET'])
def get_scheduler_list():
    """Mendapatkan daftar event scheduler lama beserta audit risikonya."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT event_group, event_name, time, command_type, target_path, target_exists, risk_level, status, recommended_action, notes FROM scheduler_events")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/cartwall-list', methods=['GET'])
def get_cartwall_list():
    """Mendapatkan daftar tab cart wall beserta rencana penataan baru."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT current_tab, slot, label, duration_seconds, current_path, detected_type, new_tab, new_folder, status, notes FROM cart_wall_items")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/playlist-audit-list', methods=['GET'])
def get_playlist_audit_list():
    """Mendapatkan rincian audit playlist lama stasiun radio."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT playlist_path, playlist_name, total_items, missing_items, dangerous_items, status, recommendation FROM playlist_audit")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == '__main__':
    # Pastikan database terbuat dan terisi skema
    init_db()
    logging.info("RadioBOSS Fresh Reset Manager server dimulai.")
    app.run(host='0.0.0.0', port=5000, debug=True)
