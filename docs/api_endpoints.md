# API Endpoints Dompetku

Base URL default: `http://localhost:5000`

## Catatan Autentikasi

- Endpoint `POST /api/auth/login` tidak membutuhkan token.
- Endpoint `POST /api/auth/logout` membutuhkan token JWT aktif.
- Endpoint fitur lain (`/api/pemasukan`, `/api/pengeluaran`, dll) tetap dilindungi `@jwt_required()`.
- Header otorisasi yang dipakai: `Authorization: Bearer <access_token>`.

## Health Check

- `GET /` - Cek API hidup

## Auth
- `POST /api/auth/login` - Login dengan `username` + `password`, menghasilkan `access_token` dan `refresh_token`
- `POST /api/auth/logout` - Logout user dan revoke token yang sedang dipakai

Payload login:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

## Pemasukan
- `GET /api/pemasukan/` - Ambil semua pemasukan
- `POST /api/pemasukan/` - Tambah pemasukan baru
- `PUT /api/pemasukan/<id>` - Update pemasukan
- `DELETE /api/pemasukan/<id>` - Hapus pemasukan

Payload minimum `POST/PUT`:

```json
{
  "jumlah": 500000,
  "tanggal": "2026-02-01"
}
```

## Pengeluaran
- `GET /api/pengeluaran/` - Ambil semua pengeluaran
- `POST /api/pengeluaran/` - Tambah pengeluaran baru
- `PUT /api/pengeluaran/<id>` - Update pengeluaran
- `DELETE /api/pengeluaran/<id>` - Hapus pengeluaran

Payload minimum `POST/PUT`:

```json
{
  "jumlah": 120000,
  "tanggal": "2026-02-01"
}
```

## Kategori
- `GET /api/kategori/` - Ambil semua kategori
- `POST /api/kategori/` - Tambah kategori baru
- `PUT /api/kategori/<id>` - Update kategori
- `DELETE /api/kategori/<id>` - Hapus kategori

Payload minimum `POST/PUT`:

```json
{
  "nama": "Gaji",
  "tipe": "pemasukan"
}
```

## Saldo
- `GET /api/saldo/` - Ambil saldo terkini

## Rekap
- `GET /api/rekap/bulanan?bulan=<bulan>&tahun=<tahun>` - Rekap bulanan

## Statistik
- `GET /api/statistik/` - Ringkasan statistik (default tahun berjalan)
- `GET /api/statistik/?tahun=<tahun>` - Ringkasan statistik tahun tertentu
