import os
import sqlite3
import json

def get_db_path():
    """Mengambil jalur file database dari app_config.json."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'app_config.json')
    db_default_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'radioboss_fresh_reset.sqlite')
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                db_rel_path = config.get("databasePath", "db/radioboss_fresh_reset.sqlite")
                # Gabungkan dengan root folder aplikasi
                root_dir = os.path.dirname(os.path.dirname(__file__))
                full_path = os.path.abspath(os.path.join(root_dir, db_rel_path))
                # Pastikan direktori database ada
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                return full_path
        except Exception:
            pass
            
    os.makedirs(os.path.dirname(db_default_path), exist_ok=True)
    return db_default_path

def get_db_connection():
    """Membuka koneksi ke database SQLite dan mengembalikan objek koneksinya."""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Menginisialisasi database dengan menjalankan schema.sql jika tabel belum ada."""
    db_path = get_db_path()
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Skema SQL tidak ditemukan di {schema_path}")
        
    conn = get_db_connection()
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def clear_all_tables():
    """Menghapus semua data dari seluruh tabel database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM file_index")
        cursor.execute("DELETE FROM playlist_audit")
        cursor.execute("DELETE FROM playlist_items")
        cursor.execute("DELETE FROM scheduler_events")
        cursor.execute("DELETE FROM cart_wall_items")
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    # Test inisialisasi
    init_db()
    print("Database berhasil diinisialisasi di:", get_db_path())
