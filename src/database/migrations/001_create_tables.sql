-- Migration 001: Buat semua tabel awal Dompetku
-- Jalankan file ini pertama kali untuk setup database

CREATE DATABASE IF NOT EXISTS dompetku CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dompetku;

CREATE TABLE IF NOT EXISTS kategori (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    tipe ENUM('pemasukan', 'pengeluaran') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pemasukan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jumlah DECIMAL(15,2) NOT NULL,
    deskripsi TEXT,
    kategori_id INT,
    tanggal DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kategori_id) REFERENCES kategori(id)
);

CREATE TABLE IF NOT EXISTS pengeluaran (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jumlah DECIMAL(15,2) NOT NULL,
    deskripsi TEXT,
    kategori_id INT,
    tanggal DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kategori_id) REFERENCES kategori(id)
);
