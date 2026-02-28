# User Manual Dompetku

Dokumen ini menjelaskan cara menggunakan API Dompetku.
Saat ini frontend belum terisi, jadi interaksi dilakukan via HTTP client
(Postman, Insomnia, curl, atau aplikasi frontend sendiri).

## 1. Cek API Aktif

Request:

```http
GET /
```

Response:

```text
Dompetku API is running!
```

## 2. Header Wajib Untuk Endpoint API

Semua endpoint `/api/*` butuh JWT.

```http
Authorization: Bearer <token>
Content-Type: application/json
```

## 3. Kelola Kategori

- `GET /api/kategori/`
- `POST /api/kategori/`
- `PUT /api/kategori/<id>`
- `DELETE /api/kategori/<id>`

Contoh tambah kategori:

```json
{
  "nama": "Gaji",
  "tipe": "pemasukan"
}
```

## 4. Kelola Pemasukan

- `GET /api/pemasukan/`
- `POST /api/pemasukan/`
- `PUT /api/pemasukan/<id>`
- `DELETE /api/pemasukan/<id>`

Contoh tambah pemasukan:

```json
{
  "jumlah": 5000000,
  "deskripsi": "Gaji bulanan",
  "kategori_id": 1,
  "tanggal": "2026-02-01"
}
```

## 5. Kelola Pengeluaran

- `GET /api/pengeluaran/`
- `POST /api/pengeluaran/`
- `PUT /api/pengeluaran/<id>`
- `DELETE /api/pengeluaran/<id>`

Contoh tambah pengeluaran:

```json
{
  "jumlah": 120000,
  "deskripsi": "Belanja mingguan",
  "kategori_id": 4,
  "tanggal": "2026-02-03"
}
```

## 6. Lihat Saldo

Endpoint:

```http
GET /api/saldo/
```

Contoh response:

```json
{
  "saldo_akhir": "4880000.00"
}
```

## 7. Rekap Bulanan

Endpoint:

```http
GET /api/rekap/bulanan?bulan=2&tahun=2026
```

Response berisi total pemasukan, total pengeluaran, saldo akhir, dan rincian
per kategori.

## 8. Statistik Tahunan

Endpoint:

```http
GET /api/statistik/?tahun=2026
```

Jika parameter `tahun` tidak dikirim, backend memakai tahun berjalan.

## 9. Catatan Penting

- Endpoint auth/login JWT belum tersedia di repository saat ini.
- Nilai uang dikembalikan sebagai string untuk konsistensi serialisasi.
