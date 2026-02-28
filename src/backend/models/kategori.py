"""Model kategori transaksi."""

from config import db
from datetime import datetime


class Kategori(db.Model):
    """Representasi kategori untuk pemasukan atau pengeluaran."""

    # Nama tabel pada database MySQL.
    __tablename__ = "kategori"

    # Primary key auto increment.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Nama kategori, misalnya "Gaji" atau "Makan".
    nama = db.Column(db.String(100), nullable=False)
    # Jenis kategori dibatasi ke dua nilai valid.
    tipe = db.Column(db.Enum("pemasukan", "pengeluaran"), nullable=False)
    # Waktu data dibuat, otomatis diisi saat insert.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """Memudahkan debugging saat objek dicetak di log/console."""
        return f"<Kategori {self.nama}>"

