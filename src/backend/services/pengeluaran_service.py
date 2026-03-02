"""Business logic untuk fitur pengeluaran."""

from models.pengeluaran import Pengeluaran
from config import db


def get_pengeluaran(user_id):
    """Mengambil semua data pengeluaran berdasarkan user_id."""
    try:
        if user_id:
            pengeluaran = Pengeluaran.query.filter_by(user_id=user_id).all()
        else:
            pengeluaran = Pengeluaran.query.filter_by(user_id=None).all()
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
            for p in pengeluaran
        ]
    except Exception as e:
        print(f"Error getting expenses: {e}")
        return []


def create_pengeluaran(data, user_id):
    """Membuat transaksi pengeluaran baru."""
    try:
        # Ambil field wajib dan opsional dari payload.
        new_pengeluaran = Pengeluaran(
            jumlah=data["jumlah"],
            deskripsi=data.get("deskripsi"),
            kategori_id=data.get("kategori_id"),
            tanggal=data["tanggal"],
            user_id=user_id,
        )
        db.session.add(new_pengeluaran)
        db.session.commit()

        return {
            "id": new_pengeluaran.id,
            "jumlah": str(new_pengeluaran.jumlah),
            "deskripsi": new_pengeluaran.deskripsi,
            "kategori_id": new_pengeluaran.kategori_id,
            "tanggal": new_pengeluaran.tanggal,
            "created_at": new_pengeluaran.created_at,
        }
    except Exception as e:
        db.session.rollback()
        print(f"Error creating expense: {e}")
        return None


def update_pengeluaran(id, data, user_id):
    """Memperbarui transaksi pengeluaran berdasarkan ID."""
    try:
        pengeluaran = Pengeluaran.query.filter_by(id=id, user_id=user_id).first()
        if not pengeluaran:
            return None

        # Update parsial, hanya field yang dikirim user.
        if "jumlah" in data:
            pengeluaran.jumlah = data["jumlah"]
        if "deskripsi" in data:
            pengeluaran.deskripsi = data["deskripsi"]
        if "kategori_id" in data:
            pengeluaran.kategori_id = data["kategori_id"]
        if "tanggal" in data:
            pengeluaran.tanggal = data["tanggal"]

        db.session.commit()
        return {
            "id": pengeluaran.id,
            "jumlah": str(pengeluaran.jumlah),
            "deskripsi": pengeluaran.deskripsi,
            "kategori_id": pengeluaran.kategori_id,
            "tanggal": pengeluaran.tanggal,
            "created_at": pengeluaran.created_at,
        }
    except Exception as e:
        db.session.rollback()
        print(f"Error updating expense: {e}")
        return None


def delete_pengeluaran(id, user_id):
    """Menghapus transaksi pengeluaran berdasarkan ID."""
    try:
        pengeluaran = Pengeluaran.query.filter_by(id=id, user_id=user_id).first()
        if not pengeluaran:
            return False

        db.session.delete(pengeluaran)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting expense: {e}")
        return False

