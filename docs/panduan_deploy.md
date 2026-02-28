# Panduan Deploy

## Prasyarat

- Docker + Docker Compose
- File `.env` (buat dari `.env.example`)

## Opsi 1 (Direkomendasikan): Deploy via Docker Compose

1. Salin environment:
   - Linux/macOS: `cp .env.example .env`
   - Windows PowerShell: `Copy-Item .env.example .env`
2. Build image:
   - `docker compose build`
3. Jalankan semua service:
   - `docker compose up -d`
4. Akses service:
   - Backend API: `http://localhost:5000`
   - phpMyAdmin: `http://localhost:8080`

Service yang dijalankan:

- `db` (MySQL 8)
- `backend` (Flask API)
- `phpmyadmin`

## Opsi 2: Menggunakan Makefile

- `make setup` untuk setup awal
- `make run` untuk start semua service
- `make stop` untuk stop service
- `make logs` untuk lihat log backend
- `make test` untuk menjalankan unit test

## Opsi 3: Windows Launcher

Jalankan `run.bat`, lalu pilih menu:

- setup
- run
- stop
- logs
- reset database

## Menjalankan Backend Tanpa Docker (Opsional)

1. Buat virtual environment dan aktifkan.
2. Install dependencies: `pip install -r requirements.txt`.
3. Pastikan MySQL aktif dan variable `.env` sesuai.
4. Jalankan: `python src/backend/main.py`.

## Catatan Frontend

Folder `src/frontend` masih placeholder, jadi proses deploy saat ini fokus pada backend API.
