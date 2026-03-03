# Dompetku 💰

Aplikasi pencatatan keuangan pribadi berbasis web (REST API + Frontend).

## Daftar Isi

- [Deskripsi](#deskripsi)
- [Fitur](#fitur)
- [Teknologi](#teknologi)
- [Struktur Proyek](#struktur-proyek)
- [Prasyarat](#prasyarat)
- [Instalasi](#instalasi)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Deployment](#deployment)
- [Dokumentasi Lengkap](#dokumentasi-lengkapsekarang)
- [Lisensi](#lisensi)

---

## Deskripsi

Dompetku adalah aplikasi pencatatan keuangan pribadi yang membantu Anda mengelola pemasukan dan pengeluaran dengan mudah. Aplikasi ini menyediakan REST API berbasis Flask dengan autentikasi JWT untuk keamanan data.

## Fitur

### Fitur Utama
- ✅ **CRUD Kategori** - Kelola kategori transaksi (pemasukan/pengeluaran)
- ✅ **CRUD Pemasukan** - Tambah, lihat, edit, hapus transaksi pemasukan
- ✅ **CRUD Pengeluaran** - Tambah, lihat, edit, hapus transaksi pengeluaran
- ✅ **Perhitungan Saldo Otomatis** - Saldo dihitung secara real-time
- ✅ **Rekap Bulanan** - Laporan keuangan per bulan dengan rincian per kategori
- ✅ **Statistik Tahunan** - Grafik tren dan distribusi kategori per tahun
- ✅ **Autentikasi JWT** - Keamanan data dengan token berbasis JSON Web Token

### Fitur Tambahan
- REST API yang siap dikonsumsi frontend manapun
- Containerization dengan Docker
- Unit test dengan Pytest
- Struktur modular (Routes → Services → Models)

---

## Teknologi

### Backend
- **Python 3.12** - Bahasa pemrograman
- **Flask 3.x** - Framework web dan API
- **Flask-SQLAlchemy** - ORM untuk akses database
- **Flask-JWT-Extended** - Autentikasi berbasis JWT
- **Flask-Migrate** - Migrasi schema database
- **marshmallow** - Serialisasi dan validasi data

### Database
- **MySQL 8** - Database server
- **PyMySQL** - Driver koneksi MySQL

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Orkestrasi container
- **Gunicorn** - WSGI server untuk production
- **phpMyAdmin** - GUI untuk database (development)

### Frontend
- **HTML5/CSS3/JavaScript** - Template dan assets
- **Flask Templates** - Server-side rendering

---

## Struktur Proyek

```
dompetku/
├── .github/                  # Konfigurasi CI/CD (GitHub Actions)
├── docs/                     # Dokumentasi proyek
│   ├── alur_kerja.md         # Alur pengembangan tim
│   ├── api_endpoints.md      # Referensi lengkap API
│   ├── deskripsi_proyek.md  # Deskripsi proyek
│   ├── panduan_deploy.md    # Panduan deployment
│   ├── design/
│   │   ├── database-schema.md
│   │   └── flowchart.md
│   ├── development/
│   │   ├── branching-strategy.md
│   │   └── coding-standards.md
│   └── user-guide/
│       ├── installation.md
│       └── user-manual.md
├── src/
│   ├── backend/              # Kode sumber backend (Flask)
│   │   ├── main.py           # Entry point aplikasi
│   │   ├── config.py         # Konfigurasi global
│   │   ├── models/           # Model SQLAlchemy
│   │   ├── routes/           # Endpoint API
│   │   ├── services/         # Logika bisnis
│   │   └── utils/            # Utility functions
│   ├── database/             # File database
│   │   ├── migrations/       # SQL migration scripts
│   │   └── seeds/            # Data awal
│   └── frontend/             # Kode sumber frontend
│       ├── app.py            # Aplikasi Flask frontend
│       ├── assets/           # CSS, JS, assets
│       ├── components/       # Komponen HTML
│       └── pages/            # Halaman web
├── tests/                    # Unit test (Pytest)
├── .env.example              # Template konfigurasi environment
├── docker-compose.yml        # Konfigurasi Docker Compose
├── Dockerfile.backend        # Dockerfile untuk backend
├── Makefile                  # Perintah shortcut
└── requirements.txt          # Dependencies Python
```

---

## Prasyarat

Sebelum memulai, pastikan sistem Anda memenuhi prasyarat berikut:

| Software | Versi Minimal |
|----------|----------------|
| Python   | 3.12           |
| Docker   | Latest          |
| Docker Compose | Latest    |
| MySQL    | 8.0            |

---

## Instalasi

### Opsi 1: Menggunakan Docker Compose (Direkomendasikan)

1. **Clone repository dan masuk ke direktori proyek**
   ```bash
   cd dompetku
   ```

2. **Salin file environment**
   ```bash
   # Linux/macOS
   cp .env.example .env
   
   # Windows (PowerShell)
   Copy-Item .env.example .env
   ```

3. **Build dan jalankan container**
   ```bash
   docker compose build
   docker compose up -d
   ```

4. **Verifikasi layanan**
   - Backend API: http://localhost:5000
   - phpMyAdmin: http://localhost:8080

### Opsi 2: Menggunakan Makefile

```bash
make setup
make run
```

### Opsi 3: Lokal (Tanpa Docker)

1. **Buat virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/macOS
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database MySQL**
   - Buat database dengan nama `dompetku`
   - Import file `src/database/migrations/001_create_tables.sql`

4. **Konfigurasi file .env**
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=dompetku
   DB_USER=dompetku_user
   DB_PASSWORD=dompetku_pass
   DB_ROOT_PASSWORD=rootpassword
   APP_PORT=5000
   APP_DEBUG=true
   SECRET_KEY=your-secret-key
   ```

5. **Jalankan aplikasi**
   ```bash
   python src/backend/main.py
   ```

---

## Menjalankan Aplikasi

### Docker Compose

```bash
# Jalankan semua service
docker compose up -d

# Lihat logs
docker compose logs -f

# Stop service
docker compose down
```

### Makefile

```bash
make run      # Jalankan aplikasi
make stop    # Stop aplikasi
make restart # Restart aplikasi
make logs    # Lihat logs
make reset   # Reset database
make test    # Jalankan test
```

### Akses Aplikasi

| Service | URL |
|---------|-----|
| Backend API | http://localhost:5000 |
| Health Check | http://localhost:5000/ |
| phpMyAdmin | http://localhost:8080 |

---

## API Reference

### Base URL
```
http://localhost:5000
```

### Autentikasi

Semua endpoint `/api/*` (kecuali login) membutuhkan JWT token di header:
```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Endpoint List

#### Health Check
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Cek API hidup |

#### Auth
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/logout` | Logout user |

#### Kategori
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/kategori/` | Ambil semua kategori |
| POST | `/api/kategori/` | Tambah kategori baru |
| PUT | `/api/kategori/<id>` | Update kategori |
| DELETE | `/api/kategori/<id>` | Hapus kategori |

#### Pemasukan
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/pemasukan/` | Ambil semua pemasukan |
| POST | `/api/pemasukan/` | Tambah pemasukan baru |
| PUT | `/api/pemasukan/<id>` | Update pemasukan |
| DELETE | `/api/pemasukan/<id>` | Hapus pemasukan |

#### Pengeluaran
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/pengeluaran/` | Ambil semua pengeluaran |
| POST | `/api/pengeluaran/` | Tambah pengeluaran baru |
| PUT | `/api/pengeluaran/<id>` | Update pengeluaran |
| DELETE | `/api/pengeluaran/<id>` | Hapus pengeluaran |

#### Saldo
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/saldo/` | Ambil saldo terkini |

#### Rekap
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/rekap/bulanan?bulan=<bulan>&tahun=<tahun>` | Rekap bulanan |

#### Statistik
| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/api/statistik/?tahun=<tahun>` | Ringkasan statistik |

### Contoh Request

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Tambah Pemasukan:**
```bash
curl -X POST http://localhost:5000/api/pemasukan/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"jumlah": 5000000, "deskripsi": "Gaji", "kategori_id": 1, "tanggal": "2026-03-01"}'
```

---

## Testing

### Menjalankan Unit Test

```bash
# Lokal
python -m pytest tests -v

# Docker
docker compose exec backend python -m pytest /app/../tests/ -v

# Menggunakan Makefile
make test
```

### Coverage Report

```bash
python -m pytest tests --cov=src/backend --cov-report=html
```

### File Test

- `tests/test_auth.py` - Test autentikasi
- `tests/test_kategori.py` - Test kategori
- `tests/test_pemasukan.py` - Test pemasukan
- `tests/test_pengeluaran.py` - Test pengeluaran
- `tests/test_saldo.py` - Test saldo
- `tests/test_rekap.py` - Test rekap bulanan
- `tests/test_statistik.py` - Test statistik

---

## Deployment

### Production dengan Docker

1. **Setup environment production**
   ```bash
   cp .env.example .env
   # Edit .env dengan nilai production
   ```

2. **Build image**
   ```bash
   docker compose build
   ```

3. **Jalankan di background**
   ```bash
   docker compose up -d
   ```

4. **Setup reverse proxy (opsional)**
   - Nginx sebagai reverse proxy
   - SSL/HTTPS dengan Let's Encrypt

### Menggunakan Gunicorn (Tanpa Docker)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.backend.main:app
```

---

## Dokumentasi Lengkap

Dokumentasi lengkap tersedia di folder `docs/`:

| Dokumen | Lokasi | Deskripsi |
|---------|--------|-----------|
| Deskripsi Proyek | `docs/deskripsi_proyek.md` | Overview proyek |
| Alur Kerja Tim | `docs/alur_kerja.md` | Proses pengembangan |
| API Endpoints | `docs/api_endpoints.md` | Referensi API lengkap |
| Panduan Deploy | `docs/panduan_deploy.md` | Cara deployment |
| Database Schema | `docs/design/database-schema.md` | Struktur database |
| Flowchart | `docs/design/flowchart.md` | Arsitektur sistem |
| Branching Strategy | `docs/development/branching-strategy.md` | Strategi branch |
| Coding Standards | `docs/development/coding-standards.md` | Standar kode |
| Instalasi | `docs/user-guide/installation.md` | Panduan instalasi |
| User Manual | `docs/user-guide/user-manual.md` | Cara penggunaan API |

---

## Lisensi

MIT License

---

## Kontak

Untuk pertanyaan atau saran,silakan buat issue di repository.
