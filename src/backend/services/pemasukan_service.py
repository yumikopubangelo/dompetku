"""Business logic untuk fitur pemasukan."""

from models.pemasukan import Pemasukan
from config import db


def get_pemasukan(user_id):
    """Mengambil semua data pemasukan berdasarkan user_id."""
    try:
        if user_id:
            pemasukan = Pemasukan.query.filter_by(user_id=user_id).all()
        else:
            pemasukan = Pemasukan.query.filter_by(user_id=None).all()
        # Ubah object ORM menjadi dict untuk response JSON.
        return [
            {
                "id": p.id,
                "jumlah": str(p.jumlah),
                "deskripsi": p.deskripsi,
                "kategori_id": p.kategori_id,
                "tanggal": p.tanggal,
                "created_at": p.created_at,
            }
            for p in pemasukan
        ]
    except Exception as e:
        print(f"Error getting income: {e}")
        return []


def create_pemasukan(data, user_id):
    """Membuat transaksi pemasukan baru."""
    try:
        # Ambil field wajib dan opsional dari payload.
        new_pemasukan = Pemasukan(
            jumlah=data["jumlah"],
            deskripsi=data.get("deskripsi"),
            kategori_id=data.get("kategori_id"),
            tanggal=data["tanggal"],
            user_id=user_id,
        )
        db.session.add(new_pemasukan)
        db.session.commit()

        return {
            "id": new_pemasukan.id,
            "jumlah": str(new_pemasukan.jumlah),
            "deskripsi": new_pemasukan.deskripsi,
            "kategori_id": new_pemasukan.kategori_id,
            "tanggal": new_pemasukan.tanggal,
            "created_at": new_pemasukan.created_at,
        }
    except Exception as e:
        db.session.rollback()
        print(f"Error creating income: {e}")
        return None


def update_pemasukan(id, data, user_id):
    """Memperbarui transaksi pemasukan berdasarkan ID."""
    try:
        pemasukan = Pemasukan.query.filter_by(id=id, user_id=user_id).first()
        if not pemasukan:
            return None

        # Update parsial, hanya field yang dikirim user.
        if "jumlah" in data:
            pemasukan.jumlah = data["jumlah"]
        if "deskripsi" in data:
            pemasukan.deskripsi = data["deskripsi"]
        if "kategori_id" in data:
            pemasukan.kategori_id = data["kategori_id"]
        if "tanggal" in data:
            pemasukan.tanggal = data["tanggal"]

        db.session.commit()
        return {
            "id": pemasukan.id,
            "jumlah": str(pemasukan.jumlah),
            "deskripsi": pemasukan.deskripsi,
            "kategori_id": pemasukan.kategori_id,
            "tanggal": pemasukan.tanggal,
            "created_at": pemasukan.created_at,
        }
    except Exception as e:
        db.session.rollback()
        print(f"Error updating income: {e}")
        return None


def delete_pemasukan(id, user_id):
    """Menghapus transaksi pemasukan berdasarkan ID."""
    try:
        pemasukan = Pemasukan.query.filter_by(id=id, user_id=user_id).first()
        if not pemasukan:
            return False

        db.session.delete(pemasukan)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting income: {e}")
        return False

