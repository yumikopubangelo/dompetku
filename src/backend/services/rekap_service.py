"""Business logic untuk rekap keuangan bulanan."""

from models.pemasukan import Pemasukan
from models.pengeluaran import Pengeluaran
from models.kategori import Kategori
from config import db


def get_rekap_bulanan(bulan, tahun, user_id):
    """Menghasilkan ringkasan pemasukan/pengeluaran per bulan dan per kategori berdasarkan user_id."""
    try:
        # Query total pemasukan per kategori pada bulan-tahun yang diminta.
        pemasukan_per_kategori = (
            db.session.query(
                Kategori.nama.label("kategori"),
                db.func.sum(Pemasukan.jumlah).label("total"),
            )
            .join(Pemasukan, Kategori.id == Pemasukan.kategori_id)
            .filter(
                db.func.month(Pemasukan.tanggal) == bulan,
                db.func.year(Pemasukan.tanggal) == tahun,
                Kategori.tipe == "pemasukan",
                Kategori.user_id == user_id,
            )
            .group_by(Kategori.nama)
            .all()
        )

        # Query total pengeluaran per kategori pada bulan-tahun yang diminta.
        pengeluaran_per_kategori = (
            db.session.query(
                Kategori.nama.label("kategori"),
                db.func.sum(Pengeluaran.jumlah).label("total"),
            )
            .join(Pengeluaran, Kategori.id == Pengeluaran.kategori_id)
            .filter(
                db.func.month(Pengeluaran.tanggal) == bulan,
                db.func.year(Pengeluaran.tanggal) == tahun,
                Kategori.tipe == "pengeluaran",
                Kategori.user_id == user_id,
            )
            .group_by(Kategori.nama)
            .all()
        )

        # Total pemasukan dan pengeluaran untuk bulan yang sama.
        total_pemasukan = (
            db.session.query(db.func.sum(Pemasukan.jumlah))
            .filter(
                db.func.month(Pemasukan.tanggal) == bulan, 
                db.func.year(Pemasukan.tanggal) == tahun,
                Pemasukan.user_id == user_id
            )
            .scalar()
            or 0
        )

        total_pengeluaran = (
            db.session.query(db.func.sum(Pengeluaran.jumlah))
            .filter(
                db.func.month(Pengeluaran.tanggal) == bulan, 
                db.func.year(Pengeluaran.tanggal) == tahun,
                Pengeluaran.user_id == user_id
            )
            .scalar()
            or 0
        )

        # Saldo akhir bulan dihitung dari selisih pemasukan dan pengeluaran.
        saldo_akhir = total_pemasukan - total_pengeluaran

        # Susun payload response terstruktur untuk route.
        rekap = {
            "bulan": bulan,
            "tahun": tahun,
            "total_pemasukan": str(total_pemasukan),
            "total_pengeluaran": str(total_pengeluaran),
            "saldo_akhir": str(saldo_akhir),
            "pemasukan_per_kategori": [{"kategori": row.kategori, "total": str(row.total)} for row in pemasukan_per_kategori],
            "pengeluaran_per_kategori": [{"kategori": row.kategori, "total": str(row.total)} for row in pengeluaran_per_kategori],
        }

        return rekap
    except Exception as e:
        print(f"Error getting monthly report: {e}")
        raise e

