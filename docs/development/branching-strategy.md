# Branching Strategy Dompetku

## Branch Utama

- `main`: branch stabil untuk rilis
- `development`: branch integrasi sebelum rilis

## Branch Kerja

- `feature/<nama-fitur>`: fitur baru
- `fix/<nama-perbaikan>`: bugfix reguler
- `hotfix/<nama-fix>`: perbaikan darurat untuk `main`

## Aturan Praktis

1. Selalu buat branch baru dari `development`.
2. Satu branch untuk satu scope perubahan.
3. Nama branch harus deskriptif dan konsisten.
4. Update test dan dokumen dalam PR yang sama.
5. Hindari commit langsung ke `main` dan `development`.

## Alur Merge

1. `feature/*` atau `fix/*` -> Pull Request ke `development`.
2. Setelah stabil, `development` -> Pull Request ke `main`.
3. `hotfix/*` bisa merge ke `main`, lalu di-backmerge ke `development`.
