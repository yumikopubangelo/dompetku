# Instalasi Dompetku

## Metode 1 (Direkomendasikan): Docker

### 1. Persiapan

- Install Docker Desktop
- Pastikan `docker compose` bisa dijalankan

### 2. Setup Environment

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### 3. Jalankan Aplikasi

```bash
docker compose build
docker compose up -d
```

### 4. Verifikasi

- API: `http://localhost:5000/`
- phpMyAdmin: `http://localhost:8080/`

## Metode 2: Makefile

```bash
make setup
make run
```

## Metode 3: Script Windows

Jalankan `run.bat`, lalu pilih menu setup dan run.

## Menjalankan Test

- Lokal: `python -m pytest tests -v`
- Docker: `docker compose exec backend python -m pytest /app/../tests/ -v`
