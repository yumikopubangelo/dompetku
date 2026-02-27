from models.pemasukan import Pemasukan
from models.pengeluaran import Pengeluaran
from config import db

def get_saldo_akhir():
    """
    Menghitung saldo akhir berdasarkan total pemasukan dan pengeluaran
    """
    try:
        total_pemasukan = db.session.query(db.func.sum(Pemasukan.jumlah)).scalar() or 0
        total_pengeluaran = db.session.query(db.func.sum(Pengeluaran.jumlah)).scalar() or 0
        
        saldo_akhir = total_pemasukan - total_pengeluaran
        
        return saldo_akhir
        
    except Exception as e:
        print(f"Error calculating final balance: {e}")
        raise e
