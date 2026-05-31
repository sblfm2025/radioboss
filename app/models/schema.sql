-- Tabel untuk menyimpan index file hasil scan
CREATE TABLE IF NOT EXISTS file_index (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_path TEXT UNIQUE,
    file_name TEXT,
    extension TEXT,
    size_bytes INTEGER,
    modified_at TEXT,
    detected_type TEXT,
    risk_level TEXT,
    status TEXT,
    recommended_folder TEXT,
    notes TEXT,
    file_hash TEXT  -- Hash MD5 untuk deteksi duplikat stasiun radio
);

-- Tabel untuk hasil audit playlist lama
CREATE TABLE IF NOT EXISTS playlist_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_path TEXT UNIQUE,
    playlist_name TEXT,
    total_items INTEGER,
    missing_items INTEGER,
    dangerous_items INTEGER,
    status TEXT,
    recommendation TEXT
);

-- Tabel rincian item dalam playlist
CREATE TABLE IF NOT EXISTS playlist_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playlist_path TEXT,
    item_path TEXT,
    resolved_path TEXT,
    file_exists INTEGER,
    detected_type TEXT,
    risk_level TEXT,
    status TEXT,
    notes TEXT
);

-- Tabel untuk event scheduler lama yang diimpor
CREATE TABLE IF NOT EXISTS scheduler_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_group TEXT,
    event_name TEXT,
    time TEXT,
    command_type TEXT,
    target_path TEXT,
    target_exists INTEGER,
    risk_level TEXT,
    status TEXT,
    recommended_action TEXT,
    notes TEXT
);

-- Tabel untuk rencana penataan Cart Wall
CREATE TABLE IF NOT EXISTS cart_wall_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    current_tab TEXT,
    slot INTEGER,
    label TEXT,
    duration_seconds REAL,
    current_path TEXT,
    detected_type TEXT,
    new_tab TEXT,
    new_folder TEXT,
    status TEXT,
    notes TEXT
);
