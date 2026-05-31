import os
import json
import logging
from flask import Blueprint, jsonify, request

# Impor instance Task Queue global dan modul service layer
from app import task_queue
from db.database import get_db_connection, clear_all_tables
from app.services.scanner_service import ScannerService
from app.services.playlist_audit_service import PlaylistAuditService
from app.services.scheduler_service import SchedulerService
from app.services.copy_service import CopyService
from app.services.report_service import ReportService
from app.services.backup_service import BackupService
from core.fresh_folder_builder import build_fresh_structure, load_fresh_root
from core.m3u8_generator import generate_fresh_playlists
from core.scheduler_plan_builder import generate_scheduler_plan

api_bp = Blueprint('api', __name__)

@api_bp.route('/stats', methods=['GET'])
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
        cursor.execute("SELECT COUNT(*) FROM file_index")
        stats["total_files"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE detected_type = 'music'")
        stats["music_files"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE detected_type = 'playlist'")
        stats["playlist_files"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE detected_type = 'ramadhan_only'")
        stats["ramadhan_files"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE detected_type = 'adzan'")
        stats["adzan_files"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM file_index WHERE notes LIKE '%DIRTY_METADATA%'")
        stats["dirty_metadata_files"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM playlist_audit WHERE status = 'BROKEN' OR status = 'NEEDS_RELINK'")
        stats["broken_playlists"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM playlist_items WHERE file_exists = 0")
        stats["missing_paths"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM scheduler_events WHERE risk_level IN ('HIGH', 'CRITICAL')")
        stats["emergency_scheduler_count"] = cursor.fetchone()[0]
        
        if stats["total_files"] > 0 and stats["broken_playlists"] == 0 and stats["missing_paths"] == 0:
            stats["readiness_status"] = "READY"
            
    except Exception as e:
        logging.error(f"Gagal mengambil stats dashboard: {e}")
        
    conn.close()
    return jsonify(stats)

@api_bp.route('/scan', methods=['POST'])
def run_scan():
    """Memicu pemindaian direktori secara asinkron lewat Task Queue."""
    data = request.json or {}
    scan_folder = data.get("folder")
    
    if not scan_folder:
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'app_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                scan_folder = json.load(f).get("defaultScanFolder", "D:\\RADIO_MUSIC_INPUT_DEMO")
                
    if not os.path.exists(scan_folder):
        return jsonify({"status": "ERROR", "message": f"Folder input '{scan_folder}' tidak ditemukan."}), 400
        
    try:
        # Pendaftaran tugas pemindaian ke Worker Thread latar belakang
        task_id = task_queue.add_task(
            "Pemindaian Pustaka & Audit Aset",
            cls_target_helper,
            scan_folder
        )
        return jsonify({"status": "PENDING", "task_id": task_id, "message": "Pendaftaran antrean scan sukses."})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

def cls_target_helper(scan_folder, progress_callback=None):
    """Fungsi helper asinkron untuk menjalankan rangkaian scan + audit secara serial."""
    ScannerService.scan_and_index(scan_folder, progress_callback=progress_callback)
    
    if progress_callback:
        progress_callback(95, "Mengaudit event scheduler & tab cart wall...")
        
    PlaylistAuditService.audit_and_relink_playlists()
    SchedulerService.analyze_events()
    generate_cart_wall_plan()
    return "SUCCESS"

@api_bp.route('/task/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Endpoint polling status tugas asinkron untuk update progres bar di UI."""
    status = task_queue.get_status(task_id)
    if not status:
        return jsonify({"status": "NOT_FOUND", "message": "Tugas tidak ditemukan."}), 404
    return jsonify(status)

@api_bp.route('/build-structure', methods=['POST'])
def build_structure():
    """Memicu pembangunan folder steril stasiun radio."""
    try:
        fresh_root, count = build_fresh_structure()
        return jsonify({"status": "SUCCESS", "fresh_root": fresh_root, "created_folders": count})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@api_bp.route('/copy-files', methods=['POST'])
def copy_files():
    """Memicu Safe Copy migrasi file secara asinkron."""
    try:
        fresh_root = load_fresh_root()
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'app_config.json')
        source_dir = "D:\\RADIO_MUSIC_INPUT_DEMO"
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                source_dir = json.load(f).get("defaultScanFolder", "D:\\RADIO_MUSIC_INPUT_DEMO")
                
        # 1. Pemicuan backup zip otomatis secara protektif sebelum penyalinan fisik
        BackupService.create_backup(source_dir, fresh_root)
        
        # 2. Pendaftaran tugas migrasi Safe Copy asinkron
        task_id = task_queue.add_task(
            "Migrasi Safe Copy & Relink Aset",
            cls_copy_helper
        )
        return jsonify({"status": "PENDING", "task_id": task_id, "message": "Proses migrasi aset dimulai."})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

def cls_copy_helper(progress_callback=None):
    """Fungsi helper asinkron untuk menjalankan migrasi Safe Copy."""
    return CopyService.migrate_approved_files(progress_callback=progress_callback)

@api_bp.route('/generate-playlists', methods=['POST'])
def build_playlists():
    """Memicu pembuatan playlist baru steril stasiun radio."""
    try:
        count = generate_fresh_playlists()
        return jsonify({"status": "SUCCESS", "created_playlists": count})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

app_bp_route_dummy = None # penanda routing dummy

@api_bp.route('/generate-scheduler-plan', methods=['POST'])
def build_scheduler_plan():
    """Memicu pembuatan rencana scheduler yang baru."""
    try:
        count = generate_scheduler_plan()
        return jsonify({"status": "SUCCESS", "events_created": count})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@api_bp.route('/generate-reports', methods=['POST'])
def build_reports():
    """Memicu pembuatan laporan secara asinkron."""
    try:
        task_id = task_queue.add_task(
            "Ekspor Seluruh Laporan CSV/MD",
            cls_report_helper
        )
        return jsonify({"status": "PENDING", "task_id": task_id, "message": "Ekspor laporan dimulai."})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

def cls_report_helper(progress_callback=None):
    """Fungsi helper asinkron untuk ekspor laporan."""
    return ReportService.generate_all_reports(progress_callback=progress_callback)

@api_bp.route('/reset-data', methods=['POST'])
def reset_db_data():
    """Mereset seluruh data di tabel SQLite stasiun radio."""
    try:
        clear_all_tables()
        return jsonify({"status": "SUCCESS", "message": "Database berhasil dikosongkan."})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@api_bp.route('/scheduler-list', methods=['GET'])
def get_scheduler_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT event_group, event_name, time, command_type, target_path, target_exists, risk_level, status, recommended_action, notes FROM scheduler_events")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@api_bp.route('/cartwall-list', methods=['GET'])
def get_cartwall_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT current_tab, slot, label, duration_seconds, current_path, detected_type, new_tab, new_folder, status, notes FROM cart_wall_items")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@api_bp.route('/playlist-audit-list', methods=['GET'])
def get_playlist_audit_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT playlist_path, playlist_name, total_items, missing_items, dangerous_items, status, recommendation FROM playlist_audit")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])
