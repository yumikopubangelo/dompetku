# Deskripsi Proyek Dompetku

Dompetku adalah aplikasi pencatatan keuangan pribadi berbasis API Flask.
Fokus utama aplikasi saat ini ada di backend: pencatatan transaksi,
pengelolaan kategori, perhitungan saldo, rekap bulanan, dan statistik tahunan.

## Fitur Yang Sudah Tersedia

- CRUD kategori transaksi (`pemasukan` dan `pengeluaran`)
- CRUD transaksi pemasukan
- CRUD transaksi pengeluaran
- Hitung saldo akhir otomatis
- Rekap bulanan per kategori
- Statistik tahunan (tren bulanan + distribusi kategori)

## Stack Teknologi

- Python 3.12
- Flask
- Flask-SQLAlchemy + SQLAlchemy
- Flask-JWT-Extended
- MySQL 8
- Docker Compose
- Pytest

## Struktur Folder Aktual

```text
src/
  backend/
    main.py
    config.py
    models/
      kategori.py
      pemasukan.py
      pengeluaran.py
    routes/
      kategori.py
      pemasukan.py
      pengeluaran.py
      saldo.py
      rekap.py
      statistik.py
    services/
      kategori_service.py
      pemasukan_service.py
      pengeluaran_service.py
      saldo_service.py
      rekap_service.py
      statistik_service.py
  database/
    migrations/001_create_tables.sql
    seeds/data_awal.sql
  frontend/
    index.html
```

## Status Frontend

Folder frontend sudah tersedia tetapi implementasi UI belum terisi.
Dokumentasi penggunaan saat ini berfokus pada akses API.
