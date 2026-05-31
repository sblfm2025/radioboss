@echo off
title RadioBOSS Fresh Reset Manager Launcher
echo ==================================================
echo         RadioBOSS Fresh Reset Manager v1.0
echo ==================================================
echo Memeriksa lingkungan Python di sistem Anda...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak terdeteksi di komputer Anda!
    echo Silakan instal Python (versi 3.8 ke atas) dan centang opsi "Add Python to PATH".
    pause
    exit /b 1
)

echo.
echo Menginstal/Memperbarui dependensi Python (Flask)...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Terjadi kesalahan saat memasang dependensi.
    echo Pastikan komputer terhubung ke internet. Mencoba menjalankan server anyway...
)

echo.
echo Memulai server lokal RadioBOSS Fresh Reset Manager...
echo Silakan tunggu, browser Anda akan otomatis terbuka ke http://localhost:5000
echo.

:: Menunggu 1 detik sebelum membuka browser untuk memberi waktu Flask menyala
timeout /t 2 /nobreak >nul
start http://localhost:5000

:: Menjalankan aplikasi utama Python
python run.py

pause
