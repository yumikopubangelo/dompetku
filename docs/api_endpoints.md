# API Endpoints Dompetku

Referensi lengkap API Dompetku untuk developer.

## Base URL

```
http://localhost:5000
```

## Autentikasi

Dompetku menggunakan JWT (JSON Web Token) untuk autentikasi.

### Aturan

- Endpoint `POST /api/auth/login` tidak membutuhkan token.
- Endpoint `POST /api/auth/logout` membutuhkan token JWT aktif.
- Endpoint fitur lain (`/api/pemasukan`, `/api/pengeluaran`, dll) dilindungi dengan `@jwt_required()`.
- Header otorisasi yang dipakai: `Authorization: Bearer <access_token>`.

### Format Header

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Health Check

### GET /

Cek apakah API berjalan.

**Request:**
```http
GET /
```

**Response:**
```
Dompetku API is running!
```

---

## Auth

### POST /api/auth/login

Login user dan mendapatkan JWT token.

**Request:**
```http
POST /api/auth/login
Content-Type: application/json
```

**Payload:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (sukses):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user_id": 1
}
```

**Response (error):**
```json
{
  "msg": "Invalid username or password"
}
```

---

### POST /api/auth/logout

Logout user dan revoke token.

**Request:**
```http
POST /api/auth/logout
Authorization: Bearer <access_token>
```

**Response (sukses):**
```json
{
  "message": "Token has been revoked"
}
```

---

## Kategori

### GET /api/kategori/

Ambil semua kategori.

**Request:**
```http
GET /api/kategori/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "kategori": [
    {
      "id": 1,
      "nama": "Gaji",
      "tipe": "pemasukan",
      "created_at": "2026-01-01T00:00:00"
    },
    {
      "id": 2,
      "nama": "Makanan",
      "tipe": "pengeluaran",
      "created_at": "2026-01-01T00:00:00"
    }
  ]
}
```

---

### POST /api/kategori/

Tambah kategori baru.

**Request:**
```http
POST /api/kategori/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Payload:**
```json
{
  "nama": "Gaji",
  "tipe": "pemasukan"
}
```

**Response (sukses):**
```json
{
  "id": 1,
  "nama": "Gaji",
  "tipe": "pemasukan",
  "created_at": "2026-01-01T00:00:00"
}
```

---

### PUT /api/kategori/<id>

Update kategori.

**Request:**
```http
PUT /api/kategori/1
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Payload:**
```json
{
  "nama": "Gaji Utama",
  "tipe": "pemasukan"
}
```

---

### DELETE /api/kategori/<id>

Hapus kategori.

**Request:**
```http
DELETE /api/kategori/1
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Kategori deleted successfully"
}
```

---

## Pemasukan

### GET /api/pemasukan/

Ambil semua transaksi pemasukan.

**Request:**
```http
GET /api/pemasukan/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "pemasukan": [
    {
      "id": 1,
      "jumlah": "5000000.00",
      "deskripsi": "Gaji bulanan",
      "kategori_id": 1,
      "tanggal": "2026-02-01",
      "created_at": "2026-02-01T00:00:00"
    }
  ]
}
```

---

### POST /api/pemasukan/

Tambah transaksi pemasukan baru.

**Request:**
```http
POST /api/pemasukan/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Payload:**
```json
{
  "jumlah": 5000000,
  "deskripsi": "Gaji bulanan",
  "kategori_id": 1,
  "tanggal": "2026-02-01"
}
```

**Payload minimum:**
```json
{
  "jumlah": 500000,
  "tanggal": "2026-02-01"
}
```

**Response (sukses):**
```json
{
  "id": 1,
  "jumlah": "5000000.00",
  "deskripsi": "Gaji bulanan",
  "kategori_id": 1,
  "tanggal": "2026-02-01",
  "created_at": "2026-02-01T00:00:00"
}
```

---

### PUT /api/pemasukan/<id>

Update transaksi pemasukan.

**Request:**
```http
PUT /api/pemasukan/1
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Payload:**
```json
{
  "jumlah": 5500000,
  "deskripsi": "Gaji + Bonus",
  "kategori_id": 1,
  "tanggal": "2026-02-01"
}
```

---

### DELETE /api/pemasukan/<id>

Hapus transaksi pemasukan.

**Request:**
```http
DELETE /api/pemasukan/1
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Pemasukan deleted successfully"
}
```

---

## Pengeluaran

### GET /api/pengeluaran/

Ambil semua transaksi pengeluaran.

**Request:**
```http
GET /api/pengeluaran/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "pengeluaran": [
    {
      "id": 1,
      "jumlah": "120000.00",
      "deskripsi": "Belanja mingguan",
      "kategori_id": 2,
      "tanggal": "2026-02-03",
      "created_at": "2026-02-03T00:00:00"
    }
  ]
}
```

---

### POST /api/pengeluaran/

Tambah transaksi pengeluaran baru.

**Request:**
```http
POST /api/pengeluaran/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Payload:**
```json
{
  "jumlah": 120000,
  "deskripsi": "Belanja mingguan",
  "kategori_id": 2,
  "tanggal": "2026-02-03"
}
```

**Payload minimum:**
```json
{
  "jumlah": 120000,
  "tanggal": "2026-02-03"
}
```

**Response (sukses):**
```json
{
  "id": 1,
  "jumlah": "120000.00",
  "deskripsi": "Belanja mingguan",
  "kategori_id": 2,
  "tanggal": "2026-02-03",
  "created_at": "2026-02-03T00:00:00"
}
```

---

### PUT /api/pengeluaran/<id>

Update transaksi pengeluaran.

**Request:**
```http
PUT /api/pengeluaran/1
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Payload:**
```json
{
  "jumlah": 150000,
  "deskripsi": "Belanja bulanan",
  "kategori_id": 2,
  "tanggal": "2026-02-03"
}
```

---

### DELETE /api/pengeluaran/<id>

Hapus transaksi pengeluaran.

**Request:**
```http
DELETE /api/pengeluaran/1
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "message": "Pengeluaran deleted successfully"
}
```

---

## Saldo

### GET /api/saldo/

Ambil saldo terkini (total pemasukan - total pengeluaran).

**Request:**
```http
GET /api/saldo/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "saldo_akhir": "4880000.00"
}
```

---

## Rekap

### GET /api/rekap/bulanan

Ambil rekap keuangan bulanan.

**Request:**
```http
GET /api/rekap/bulanan?bulan=2&tahun=2026
Authorization: Bearer <access_token>
```

**Parameter:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| bulan | int | Bulan (1-12) |
| tahun | int | Tahun (misal: 2026) |

**Response:**
```json
{
  "bulan": 2,
  "tahun": 2026,
  "total_pemasukan": "5000000.00",
  "total_pengeluaran": "120000.00",
  "saldo_akhir": "4880000.00",
  "rincian_pemasukan": [
    {
      "kategori": "Gaji",
      "total": "5000000.00"
    }
  ],
  "rincian_pengeluaran": [
    {
      "kategori": "Makanan",
      "total": "120000.00"
    }
  ]
}
```

---

## Statistik

### GET /api/statistik/

Ambil ringkasan statistik tahunan.

**Request:**
```http
GET /api/statistik/?tahun=2026
Authorization: Bearer <access_token>
```

**Parameter:**
| Parameter | Tipe | Deskripsi |
|-----------|------|-----------|
| tahun | int | Tahun (opsional, default: tahun berjalan) |

**Response:**
```json
{
  "tahun": 2026,
  "total_pemasukan": "15000000.00",
  "total_pengeluaran": "5000000.00",
  "saldo_akhir": "10000000.00",
  "tren_bulanan": [
    {
      "bulan": 1,
      "pemasukan": "5000000.00",
      "pengeluaran": "1000000.00"
    },
    {
      "bulan": 2,
      "pemasukan": "5000000.00",
      "pengeluaran": "1200000.00"
    }
  ],
  "distribusi_pemasukan": [
    {
      "kategori": "Gaji",
      "total": "12000000.00",
      "persentase": 80
    }
  ],
  "distribusi_pengeluaran": [
    {
      "kategori": "Makanan",
      "total": "2000000.00",
      "persentase": 40
    }
  ]
}
```

---

## Kode Status HTTP

| Kode | Deskripsi |
|------|-----------|
| 200 | OK - Request berhasil |
| 201 | Created - Resource berhasil dibuat |
| 400 | Bad Request - Input tidak valid |
| 401 | Unauthorized - Token tidak valid |
| 404 | Not Found - Resource tidak ditemukan |
| 500 | Internal Server Error - Error di server |

---

## Catatan

- Semua nilai uang (`jumlah`, `saldo_akhir`) dikembalikan sebagai **string** untuk menjaga presisi desimal.
- Format tanggal: `YYYY-MM-DD` (contoh: `2026-02-01`).
- Semua timestamp menggunakan format ISO 8601.
