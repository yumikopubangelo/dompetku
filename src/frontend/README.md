# Frontend Dompetku

Frontend Dompetku menggunakan Python server-rendered (Flask + Jinja2).

## Konsep

- Halaman HTML dirender oleh Flask (template Jinja2)
- Asset statis (CSS/JS/gambar) disimpan di folder `assets/`
- Komponen reusable disimpan di folder `components/`
- Halaman lengkap disimpan di folder `pages/`

## Struktur Folder

```
src/frontend/
├── app.py              # Aplikasi Flask untuk frontend
├── base.html           # Template dasar
├── assets/             # Asset statis
│   ├── main.js         # JavaScript utama
│   └── style.css       # Stylesheet utama
├── components/        # Komponen HTML reusable
│   ├── alerts.html
│   ├── footer.html
│   ├── header.html
│   └── modal.html
└── pages/             # Halaman lengkap
    ├── dashboard.html
    ├── kategori.html
    ├── login.html
    ├── pemasukan.html
    ├── pengeluaran.html
    ├── register.html
    └── rekap.html
```

## Integrasi dengan Auth

- Gunakan JWT token dari response login
- Simpan token di localStorage atau cookie yang aman
- Sertakan token di header untuk setiap request ke API
- Rekomendasi: `HttpOnly` cookie untuk produksi

## Menjalankan Frontend

Frontend sudah terintegrasi dengan backend saat menjalankan `python src/frontend/app.py` atau melalui Docker Compose.
