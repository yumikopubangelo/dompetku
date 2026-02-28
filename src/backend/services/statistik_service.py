"""Business logic untuk statistik keuangan tahunan."""

from models.pemasukan import Pemasukan
from models.pengeluaran import Pengeluaran
from models.kategori import Kategori
from config import db
from datetime import datetime


def get_statistik_keuangan(tahun=None):
    """Menghasilkan statistik tren bulanan, distribusi kategori, dan total tahunan."""
    # Jika tahun tidak diberikan, gunakan tahun saat ini.
    if not tahun:
        tahun = datetime.now().year

    try:
        # Hitung tren bulanan selama 12 bulan.
        tren_bulanan = []
        for bulan in range(1, 13):
            total_pemasukan = (
                db.session.query(db.func.sum(Pemasukan.jumlah))
                .filter(db.func.month(Pemasukan.tanggal) == bulan, db.func.year(Pemasukan.tanggal) == tahun)
                .scalar()
                or 0
            )

            total_pengeluaran = (
                db.session.query(db.func.sum(Pengeluaran.jumlah))
                .filter(db.func.month(Pengeluaran.tanggal) == bulan, db.func.year(Pengeluaran.tanggal) == tahun)
                .scalar()
                or 0
            )

            tren_bulanan.append(
                {"bulan": bulan, "pemasukan": str(total_pemasukan), "pengeluaran": str(total_pengeluaran)}
            )

        # Distribusi kategori pemasukan dalam tahun yang dipilih.
        distribusi_pemasukan = (
            db.session.query(
                Kategori.nama.label("kategori"),
                db.func.sum(Pemasukan.jumlah).label("total"),
            )
            .join(Pemasukan, Kategori.id == Pemasukan.kategori_id)
            .filter(db.func.year(Pemasukan.tanggal) == tahun, Kategori.tipe == "pemasukan")
            .group_by(Kategori.nama)
            .all()
        )

        # Distribusi kategori pengeluaran dalam tahun yang dipilih.
        distribusi_pengeluaran = (
            db.session.query(
                Kategori.nama.label("kategori"),
                db.func.sum(Pengeluaran.jumlah).label("total"),
            )
            .join(Pengeluaran, Kategori.id == Pengeluaran.kategori_id)
            .filter(db.func.year(Pengeluaran.tanggal) == tahun, Kategori.tipe == "pengeluaran")
            .group_by(Kategori.nama)
            .all()
        )

        # Hitung total tahunan pemasukan dan pengeluaran.
        total_tahun_pemasukan = (
            db.session.query(db.func.sum(Pemasukan.jumlah)).filter(db.func.year(Pemasukan.tanggal) == tahun).scalar() or 0
        )

        total_tahun_pengeluaran = (
            db.session.query(db.func.sum(Pengeluaran.jumlah))
            .filter(db.func.year(Pengeluaran.tanggal) == tahun)
            .scalar()
            or 0
        )

        # Total saldo tahunan = total pemasukan tahunan - total pengeluaran tahunan.
        total_saldo_tahun = total_tahun_pemasukan - total_tahun_pengeluaran

        # Susun payload response statistik.
        statistik = {
            "tahun": tahun,
            "total_pemasukan": str(total_tahun_pemasukan),
            "total_pengeluaran": str(total_tahun_pengeluaran),
            "total_saldo": str(total_saldo_tahun),
            "tren_bulanan": tren_bulanan,
            "distribusi_pemasukan": [{"kategori": row.kategori, "total": str(row.total)} for row in distribusi_pemasukan],
            "distribusi_pengeluaran": [{"kategori": row.kategori, "total": str(row.total)} for row in distribusi_pengeluaran],
        }

        return statistik
    except Exception as e:
        print(f"Error getting financial statistics: {e}")
        raise e

