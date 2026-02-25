@echo off
echo.
echo  ============================
echo   Dompetku - Windows Launcher
echo  ============================
echo.
echo  Pilih opsi:
echo  [1] Setup awal (jalankan pertama kali)
echo  [2] Jalankan aplikasi
echo  [3] Matikan aplikasi
echo  [4] Lihat log backend
echo  [5] Reset database (data terhapus!)
echo  [6] Keluar
echo.
set /p choice=Masukkan pilihan (1-6): 

if "%choice%"=="1" goto SETUP
if "%choice%"=="2" goto RUN
if "%choice%"=="3" goto STOP
if "%choice%"=="4" goto LOGS
if "%choice%"=="5" goto RESET
if "%choice%"=="6" goto END

:SETUP
echo.
echo Menyalin .env.example ke .env ...
if not exist .env copy .env.example .env
echo Build Docker image ...
docker compose build
echo.
echo Setup selesai! Pilih opsi 2 untuk menjalankan.
pause
goto END

:RUN
echo.
echo Menjalankan semua service ...
docker compose up -d
echo.
echo Aplikasi berjalan di:
echo   Backend    -^> http://localhost:5000
echo   phpMyAdmin -^> http://localhost:8080
pause
goto END

:STOP
echo.
echo Mematikan semua service ...
docker compose down
pause
goto END

:LOGS
echo.
echo Menampilkan log backend (tekan Ctrl+C untuk keluar) ...
docker compose logs -f backend
goto END

:RESET
echo.
echo PERINGATAN: Semua data database akan dihapus!
set /p confirm=Lanjutkan? (y/N): 
if /i "%confirm%"=="y" (
    docker compose down -v
    docker compose up -d
    echo Reset selesai!
) else (
    echo Reset dibatalkan.
)
pause
goto END

:END
