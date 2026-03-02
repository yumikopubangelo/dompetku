-- Migration 003: Tambah user_id ke tabel kategori, pemasukan, pengeluaran
-- Untuk membuat data per-user (multi-tenant)

USE dompetku;

-- Tambah kolom user_id ke tabel kategori
ALTER TABLE kategori ADD COLUMN user_id INT NULL;
ALTER TABLE kategori ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
CREATE INDEX idx_kategori_user_id ON kategori(user_id);

-- Tambah kolom user_id ke tabel pemasukan
ALTER TABLE pemasukan ADD COLUMN user_id INT NULL;
ALTER TABLE pemasukan ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
CREATE INDEX idx_pemasukan_user_id ON pemasukan(user_id);

-- Tambah kolom user_id ke tabel pengeluaran
ALTER TABLE pengeluaran ADD COLUMN user_id INT NULL;
ALTER TABLE pengeluaran ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
CREATE INDEX idx_pengeluaran_user_id ON pengeluaran(user_id);
