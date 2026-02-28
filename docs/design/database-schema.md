# Database Schema Dompetku

Skema database saat ini mengikuti file:
`src/database/migrations/001_create_tables.sql`.

## Tabel `kategori`

- `id` INT, primary key, auto increment
- `nama` VARCHAR(100), wajib
- `tipe` ENUM(`pemasukan`, `pengeluaran`), wajib
- `created_at` TIMESTAMP, default current timestamp

## Tabel `pemasukan`

- `id` INT, primary key, auto increment
- `jumlah` DECIMAL(15,2), wajib
- `deskripsi` TEXT, opsional
- `kategori_id` INT, foreign key ke `kategori.id`
- `tanggal` DATE, wajib
- `created_at` TIMESTAMP, default current timestamp

## Tabel `pengeluaran`

- `id` INT, primary key, auto increment
- `jumlah` DECIMAL(15,2), wajib
- `deskripsi` TEXT, opsional
- `kategori_id` INT, foreign key ke `kategori.id`
- `tanggal` DATE, wajib
- `created_at` TIMESTAMP, default current timestamp

## Relasi

- Satu `kategori` bisa punya banyak `pemasukan`
- Satu `kategori` bisa punya banyak `pengeluaran`

## ER Diagram (Ringkas)

```mermaid
erDiagram
    KATEGORI ||--o{ PEMASUKAN : memiliki
    KATEGORI ||--o{ PENGELUARAN : memiliki

    KATEGORI {
        int id PK
        string nama
        enum tipe
        datetime created_at
    }

    PEMASUKAN {
        int id PK
        decimal jumlah
        text deskripsi
        int kategori_id FK
        date tanggal
        datetime created_at
    }

    PENGELUARAN {
        int id PK
        decimal jumlah
        text deskripsi
        int kategori_id FK
        date tanggal
        datetime created_at
    }
```
