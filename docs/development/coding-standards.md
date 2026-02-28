# Coding Standards Dompetku

## Python Style

- Gunakan PEP 8 sebagai dasar style code.
- Setiap module/function utama wajib punya docstring singkat.
- Gunakan nama fungsi/variabel yang jelas (`snake_case`).
- Hindari logika bisnis di route; simpan di `services/`.

## Struktur Layer

- `routes/`: parsing request, validasi awal, status code
- `services/`: logika bisnis dan orkestrasi query
- `models/`: definisi skema data SQLAlchemy
- `tests/`: unit test untuk route dan service

## Standar API Response

- Format response: JSON.
- Gunakan status code HTTP yang tepat (`200`, `201`, `400`, `404`, `500`).
- Untuk nilai `Decimal`, serialisasikan ke string agar konsisten.
- Error message dibuat jelas dan konsisten antar endpoint.

## Testing

- Tambah atau update test setiap ada perubahan perilaku.
- Test minimal mencakup:
  - skenario sukses
  - input tidak valid
  - not found (jika relevan)
  - error internal/service failure

Command test:

- Lokal: `python -m pytest tests -v`
- Docker: `docker compose exec backend python -m pytest /app/../tests/ -v`

## Dokumentasi

- Jika endpoint, payload, atau alur berubah, update `docs/` pada PR yang sama.
