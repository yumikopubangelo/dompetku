# Flowchart Arsitektur Request

Alur backend mengikuti pola `Route -> Service -> Model -> Database`.

```mermaid
flowchart TD
    A[Client kirim HTTP request] --> B[Flask Route Blueprint]
    B --> C{Validasi request}
    C -->|Tidak valid| D[Response 400]
    C -->|Valid| E[Service Layer]
    E --> F[Model SQLAlchemy]
    F --> G[(MySQL)]
    G --> H[Hasil query]
    H --> I[Service susun response JSON]
    I --> J[Route kembalikan status code]
    J --> K[Client terima response]
```

## Blueprint Yang Terdaftar

- `/api/kategori`
- `/api/pemasukan`
- `/api/pengeluaran`
- `/api/saldo`
- `/api/rekap`
- `/api/statistik`

## Catatan

- Semua endpoint `/api/*` membutuhkan JWT (`@jwt_required()`).
- Endpoint root `/` hanya untuk health check.
