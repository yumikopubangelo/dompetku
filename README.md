
# Dompetku 💰

Aplikasi pencatatan keuangan pribadi sederhana.

## Fitur
- Pencatatan pemasukan & pengeluaran

# Dompetku

Aplikasi pencatatan keuangan pribadi berbasis web.

## Fitur
- Pencatatan pemasukan dan pengeluaran
- Pengelompokan transaksi berdasarkan kategori
- Perhitungan saldo otomatis
- Rekap keuangan bulanan
- Ringkasan statistik keuangan
- 
## Struktur Proyek
- `src/backend/`  : Kode sumber backend (Python)
- `src/frontend/` : Kode sumber frontend (TBD)
- `tests/`        : Unit test backend
- `docs/`         : Dokumentasi proyek
- `.github/`      : Konfigurasi CI/CD (GitHub Actions)

## Cara Menjalankan Backend
_(akan diisi setelah setup selesai)_

## Dependensi
Lihat `requirements.txt`
=======
## Stack dan Library
### Aplikasi Python (Backend + Frontend)
- `Flask` untuk web app dan API
- `Flask-SQLAlchemy` + `SQLAlchemy` untuk ORM dan akses database
- `Flask-Migrate` untuk migrasi schema database
- `marshmallow` untuk serialisasi dan validasi data
- `python-dotenv` untuk konfigurasi environment (`.env`)
- `gunicorn` untuk deployment production
- `pytest` + `pytest-cov` untuk unit test dan coverage

### Autentikasi (Rekomendasi)
- `Flask-Login` untuk login berbasis session cookie
- `Flask-WTF` untuk form handling + CSRF protection
- Default arsitektur: session cookie (`HttpOnly`, `Secure`, `SameSite`)
- JWT tidak wajib untuk arsitektur ini, kecuali nanti API dipakai client terpisah (mobile/SPA/domain lain)

## Struktur Proyek
- `src/backend/` : Kode Python utama (route, service, model)
- `src/frontend/` : Template HTML/CSS/asset frontend yang dirender dari Flask
- `tests/` : Unit test backend
- `docs/` : Dokumentasi proyek
- `.github/` : Konfigurasi CI/CD (GitHub Actions)

## Menjalankan Aplikasi
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
python -m pytest tests -v

# Jalankan aplikasi (sesuaikan entrypoint final Anda)
python src/backend/main.py
```

## Dependensi
- Python dependencies: [requirements.txt](requirements.txt)
- Catatan frontend Python: [src/frontend/README.md](src/frontend/README.md)

