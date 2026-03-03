# Database Dompetku (MySQL)

Dokumen ini menjelaskan struktur database Dompetku.

## Struktur Folder

```
src/database/
├── migrations/        # File SQL untuk membuat tabel
│   ├── 001_create_tables.sql
│   ├── 002_create_users_table.sql
│   └── 003_add_user_id_columns.sql
└── seeds/             # Data awal untuk development/testing
    ├── auth_seed.sql
    └── data_awal.sql
```

## Cara Menjalankan

Jika menggunakan Docker Compose, database otomatis ter-setup saat menjalankan:

```bash
make run
# atau
docker compose up -d
```

File migration dijalankan secara otomatis melalui volume Docker yang mounting ke `/docker-entrypoint-initdb.d`.

## Struktur Tabel

### Tabel `kategori`
Menyimpan kategori transaksi (pemasukan/pengeluaran).

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| id | INT | Primary key |
| nama | VARCHAR(100) | Nama kategori |
| tipe | ENUM | Tipe: 'pemasukan' atau 'pengeluaran' |
| created_at | TIMESTAMP | Tanggal dibuat |

### Tabel `pemasukan`
Menyimpan transaksi pemasukan.

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| id | INT | Primary key |
| jumlah | DECIMAL(15,2) | Jumlah uang |
| deskripsi | TEXT | Keterangan (opsional) |
| kategori_id | INT | Foreign key ke kategori |
| tanggal | DATE | Tanggal transaksi |
| created_at | TIMESTAMP | Tanggal dibuat |

### Tabel `pengeluaran`
Menyimpan transaksi pengeluaran.

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| id | INT | Primary key |
| jumlah | DECIMAL(15,2) | Jumlah uang |
| deskripsi | TEXT | Keterangan (opsional) |
| kategori_id | INT | Foreign key ke kategori |
| tanggal | DATE | Tanggal transaksi |
| created_at | TIMESTAMP | Tanggal dibuat |

## Troubleshooting

Jika database tidak terhubung:
1. Pastikan container Docker running: `docker compose ps`
2. Cek log: `docker compose logs db`
3. Pastikan variabel environment di `.env` sesuai
