import os
import sys
import logging
from app import create_app

# Buat aplikasi menggunakan inisialisasi factory modern
app = create_app()

if __name__ == '__main__':
    logging.info("Memulai server Flask lokal RadioBOSS Fresh Reset Manager v2.0...")
    app.run(host='0.0.0.0', port=5000, debug=True)
