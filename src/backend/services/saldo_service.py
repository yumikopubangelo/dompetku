"""Business logic untuk perhitungan saldo."""

from models.pemasukan import Pemasukan
from models.pengeluaran import Pengeluaran
from config import db


def get_saldo_akhir():
    """Menghitung saldo akhir dari total pemasukan dikurangi total pengeluaran."""
    try:
        # Aggregate total pemasukan, fallback 0 jika belum ada data.
        total_pemasukan = db.session.query(db.func.sum(Pemasukan.jumlah)).scalar() or 0
        # Aggregate total pengeluaran, fallback 0 jika belum ada data.
        total_pengeluaran = db.session.query(db.func.sum(Pengeluaran.jumlah)).scalar() or 0

        # Rumus saldo akhir aplikasi.
        saldo_akhir = total_pemasukan - total_pengeluaran
        return saldo_akhir
    except Exception as e:
        print(f"Error calculating final balance: {e}")
        raise e

