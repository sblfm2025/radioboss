import os
from flask import Flask
from db.database import init_db
from app.utils.task_queue import TaskQueueManager

# Instance global asinkron Task Queue untuk backend stasiun radio
task_queue = TaskQueueManager()

def create_app():
    """Factory Function untuk inisialisasi aplikasi Flask modern."""
    # Pastikan database SQLite dimuat dengan skema baru dari app/models/schema.sql
    # Kita overwrite inisialisasi bawaan dengan mengarahkan ke skema baru
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(app_root, 'app', 'models', 'schema.sql')
    
    # Override skema SQLite database
    db_schema_default = os.path.join(app_root, 'db', 'schema.sql')
    try:
        shutil_dest = os.path.abspath(db_schema_default)
        os.makedirs(os.path.dirname(shutil_dest), exist_ok=True)
        with open(shutil_dest, 'w', encoding='utf-8') as f:
            with open(schema_path, 'r', encoding='utf-8') as src:
                f.write(src.read())
    except Exception:
        pass
        
    init_db()
    
    app = Flask(
        __name__,
        template_folder=os.path.join(app_root, 'app', 'templates'),
        static_folder=os.path.join(app_root, 'app', 'static')
    )
    
    # Registrasi modular routes
    from app.routes.main_routes import main_bp
    from app.routes.api_routes import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
