# Instalasi Dompetku

Panduan lengkap cara installing Dompetku.

## Metode 1: Docker Compose (Direkomendasikan)

Cara termudah dan tercepat untuk menjalankan Dompetku.

### 1. Persiapan

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Pastikan `docker compose` bisa dijalankan:
  ```bash
  docker --version
  docker compose version
  ```

### 2. Setup Environment

```bash
# Linux/macOS
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env
```

### 3. Konfigurasi .env

Buka file `.env` dan sesuaikan nilai berikut:

```env
# Database
DB_HOST=db
DB_PORT=3306
DB_NAME=dompetku
DB_USER=dompetku_user
DB_PASSWORD=dompetku_pass
DB_ROOT_PASSWORD=rootpassword

# Backend
APP_PORT=5000
APP_DEBUG=true
SECRET_KEY=ganti-dengan-secret-key-acak
```

### 4. Build dan Jalankan

```bash
# Build image
docker compose build

# Jalankan semua service
docker compose up -d
```

### 5. Verifikasi

Setelah container running, akses:

| Service | URL |
|---------|-----|
| Backend API | http://localhost:5000 |
| Health Check | http://localhost:5000/ |
| phpMyAdmin | http://localhost:8080 |

---

## Metode 2: Menggunakan Makefile

Jika sudah install Docker, bisa menggunakan Makefile untuk perintah yang lebih mudah.

```bash
# Setup awal (salin .env + build)
make setup

# Jalankan aplikasi
make run

# Lihat logs
make logs

# Stop aplikasi
make stop
```

---

## Metode 3: Script Windows (run.bat)

Untuk pengguna Windows, bisa menggunakan script `run.bat`:

1. Buka terminal/command prompt
2. Jalankan: `run.bat`
3. Pilih menu:
   - `1` - Setup (sama seperti `make setup`)
   - `2` - Run (sama seperti `make run`)
   - `3` - Stop (sama seperti `make stop`)
   - `4` - Logs (sama seperti `make logs`)
   - `5` - Reset database

---

## Metode 4: Lokal (Tanpa Docker)

Jika ingin menjalankan secara lokal tanpa Docker:

### 1. Persiapan

- Install Python 3.12+
- Install MySQL 8

### 2. Setup Python

```bash
# Buat virtual environment
python -m venv .venv

# Aktifkan (Windows)
.venv\Scripts\activate

# Aktifkan (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Database

1. Buka MySQL (via terminal atau phpMyAdmin)
2. Buat database:
   ```sql
   CREATE DATABASE dompetku CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Import file migration:
   ```bash
   mysql -u root -p dompetku < src/database/migrations/001_create_tables.sql
   ```

### 4. Konfigurasi .env

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=dompetku
DB_USER=root
DB_PASSWORD=your_password
APP_PORT=5000
APP_DEBUG=true
SECRET_KEY=your-secret-key
```

### 5. Jalankan Aplikasi

```bash
python src/backend/main.py
```

---

## Menjalankan Test

### Test Lokal

```bash
python -m pytest tests -v
```

### Test Docker

```bash
docker compose exec backend python -m pytest /app/../tests/ -v
```

### Test dengan Makefile

```bash
make test
```

---

## Troubleshooting

### Container tidak mau start

1. Cek apakah port sudah digunakan:
   ```bash
   netstat -an | findstr "5000"
   ```
2. Hapus container dan build ulang:
   ```bash
   docker compose down
   docker compose build --no-cache
   docker compose up -d
   ```

### Database tidak terhubung

1. Cek container berjalan: `docker compose ps`
2. Cek logs: `docker compose logs db`
3. Tunggu hingga database healthy

### Error permission

Pastikan Docker memiliki permission yang cukup untuk mount volume.
