"""Business logic untuk perhitungan saldo."""

from models.pemasukan import Pemasukan
from models.pengeluaran import Pengeluaran
from config import db


def get_saldo_akhir(user_id):
    """Menghitung saldo akhir dari total pemasukan dikurangi pengeluaran berdasarkan user_id."""
    try:
        # Aggregate total pemasukan berdasarkan user_id, fallback 0 jika belum ada data.
        total_pemasukan = db.session.query(db.func.sum(Pemasukan.jumlah)).filter(
            Pemasukan.user_id == user_id
        ).scalar() or 0
        
        # Aggregate total pengeluaran berdasarkan user_id, fallback 0 jika belum ada data.
        total_pengeluaran = db.session.query(db.func.sum(Pengeluaran.jumlah)).filter(
            Pengeluaran.user_id == user_id
        ).scalar() or 0

        # Rumus saldo akhir per user.
        saldo_akhir = total_pemasukan - total_pengeluaran
        return saldo_akhir
    except Exception as e:
        print(f"Error calculating final balance: {e}")
        raise e

