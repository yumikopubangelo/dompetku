# User Manual Dompetku

Dokumen ini menjelaskan cara menggunakan API Dompetku.
Saat ini frontend belum terisi, jadi interaksi dilakukan via HTTP client
(Postman, Insomnia, curl, atau aplikasi frontend sendiri).

## 1. Login

Sebelum menggunakan endpoint API lain, user harus login terlebih dahulu untuk mendapatkan JWT token.

Endpoint:

```http
POST /api/auth/login
```

Payload:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response (sukses):

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": 1
}
```

**Catatan:** Simpan `access_token` untuk mengakses endpoint lain, dan `refresh_token` untuk memperbarui token yang habis masa berlakunya.

## 2. Header Wajib Untuk Endpoint API

Semua endpoint `/api/*` (kecuali login) membutuhkan JWT token di header:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

## 3. Health Check

Request:

```http
GET /
```

Response:

```text
Dompetku API is running!
```

## 4. Kelola Kategori

- `GET /api/kategori/` - Ambil semua kategori
- `POST /api/kategori/` - Tambah kategori baru
- `PUT /api/kategori/<id>` - Update kategori
- `DELETE /api/kategori/<id>` - Hapus kategori

Contoh tambah kategori:

```json
{
  "nama": "Gaji",
  "tipe": "pemasukan"
}
```

## 5. Kelola Pemasukan

- `GET /api/pemasukan/` - Ambil semua pemasukan
- `POST /api/pemasukan/` - Tambah pemasukan baru
- `PUT /api/pemasukan/<id>` - Update pemasukan
- `DELETE /api/pemasukan/<id>` - Hapus pemasukan

Contoh tambah pemasukan:

```json
{
  "jumlah": 5000000,
  "deskripsi": "Gaji bulanan",
  "kategori_id": 1,
  "tanggal": "2026-02-01"
}
```

## 6. Kelola Pengeluaran

- `GET /api/pengeluaran/` - Ambil semua pengeluaran
- `POST /api/pengeluaran/` - Tambah pengeluaran baru
- `PUT /api/pengeluaran/<id>` - Update pengeluaran
- `DELETE /api/pengeluaran/<id>` - Hapus pengeluaran

Contoh tambah pengeluaran:

```json
{
  "jumlah": 120000,
  "deskripsi": "Belanja mingguan",
  "kategori_id": 4,
  "tanggal": "2026-02-03"
}
```

## 7. Lihat Saldo

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

## 8. Rekap Bulanan

Endpoint:

```http
GET /api/rekap/bulanan?bulan=2&tahun=2026
```

Response berisi total pemasukan, total pengeluaran, saldo akhir, dan rincian
per kategori.

## 9. Statistik Tahunan

Endpoint:

```http
GET /api/statistik/?tahun=2026
```

Jika parameter `tahun` tidak dikirim, backend memakai tahun berjalan.

## 10. Logout

Endpoint:

```http
POST /api/auth/logout
```

Header:

```http
Authorization: Bearer <access_token>
```

Response:

```json
{
  "message": "Token has been revoked"
}
```

## 11. Catatan Penting

- Nilai uang dikembalikan sebagai string untuk konsistensi serialisasi.
- Semua transaksi (pemasukan/pengeluaran) dapat dikaitkan dengan kategori untuk memudahkan rekap.
- Login diperlukan sebelum mengakses endpoint yang membutuhkan autentikasi.
