# Alur Kerja Tim

## Branching Strategy

- `main`: branch stabil
- `development`: branch integrasi
- `feature/<nama-fitur>`: branch kerja harian
- `hotfix/<nama-fix>`: perbaikan cepat

## Alur Pengembangan

1. Tarik perubahan terbaru dari `development`.
2. Buat branch fitur dari `development`.
3. Implementasi di layer yang sesuai (`routes`, `services`, `models`, `tests`, `docs`).
4. Jalankan test lokal:
   - `python -m pytest tests -v` (lokal)
   - atau `docker compose exec backend python -m pytest /app/../tests/ -v` (Docker)
5. Perbarui dokumentasi di folder `docs/` jika ada perubahan endpoint/arsitektur.
6. Buat pull request ke `development`.

## Alur Pull Request

1. PR berisi deskripsi perubahan, cara uji, dan dampak ke API/database.
2. Minimal 1 reviewer menyetujui.
3. Semua test wajib lulus sebelum merge.
4. Squash merge ke `development`.
5. Rilis ke `main` dilakukan berkala dari `development`.
