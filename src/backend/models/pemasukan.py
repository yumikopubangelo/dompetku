"""Model transaksi pemasukan."""

from config import db
from datetime import datetime


class Pemasukan(db.Model):
    """Representasi data pemasukan yang dicatat user."""

    # Nama tabel pada database.
    __tablename__ = "pemasukan"

    # Primary key auto increment.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Nominal pemasukan dengan presisi dua angka desimal.
    jumlah = db.Column(db.Numeric(15, 2), nullable=False)
    # Catatan tambahan transaksi (opsional).
    deskripsi = db.Column(db.Text)
    # Foreign key ke tabel kategori.
    kategori_id = db.Column(db.Integer, db.ForeignKey("kategori.id"))
    # Tanggal terjadinya transaksi.
    tanggal = db.Column(db.Date, nullable=False)
    # Waktu data dibuat.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi ke model Kategori untuk kemudahan join dan akses object.
    kategori = db.relationship("Kategori", backref=db.backref("pemasukan", lazy=True))

    def __repr__(self):
        """Memudahkan debugging saat objek pemasukan dicetak."""
        return f"<Pemasukan {self.jumlah}>"
