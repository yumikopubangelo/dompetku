# Frontend Dompetku

<<<<<<< HEAD
Folder ini diisi oleh tim frontend.
Teknologi frontend belum ditentukan - sesuaikan struktur ini
setelah framework dipilih (React, Vue, Svelte, dsb).
=======
Frontend menggunakan Python server-rendered (Flask + Jinja2), bukan React/Vite.

## Konsep
- Halaman HTML dirender oleh Flask (template Jinja2)
- Asset statis (CSS/JS/gambar) disimpan di folder frontend/static sesuai kebutuhan proyek
- Tidak membutuhkan `npm install` untuk setup dasar

## Integrasi dengan Auth
- Gunakan session cookie dari `Flask-Login`
- Lindungi form dengan CSRF token dari `Flask-WTF`
- Rekomendasi cookie: `HttpOnly`, `Secure`, `SameSite=Lax/Strict`
>>>>>>> 4631ec9 (chore: initialize project structure with src, tests, docs, and configuration)
