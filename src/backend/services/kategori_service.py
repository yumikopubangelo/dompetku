"""Business logic untuk fitur kategori."""

from models.kategori import Kategori
from config import db


def get_kategori(user_id):
    """Mengambil seluruh kategori dari database berdasarkan user_id."""
    try:
        if user_id:
            kategori = Kategori.query.filter_by(user_id=user_id).all()
        else:
            kategori = Kategori.query.filter_by(user_id=None).all()
        # Mapping objek ORM menjadi dict agar siap dijadikan JSON response.
        return [{"id": k.id, "nama": k.nama, "tipe": k.tipe, "created_at": k.created_at} for k in kategori]
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []


def create_kategori(data, user_id):
    """Membuat kategori baru."""
    try:
        # Membangun objek model dari payload request.
        new_kategori = Kategori(nama=data["nama"], tipe=data["tipe"], user_id=user_id)
        db.session.add(new_kategori)
        db.session.commit()

        return {
            "id": new_kategori.id,
            "nama": new_kategori.nama,
            "tipe": new_kategori.tipe,
            "created_at": new_kategori.created_at,
        }
    except Exception as e:
        # Rollback penting agar transaksi yang gagal tidak mengunci session.
        db.session.rollback()
        print(f"Error creating category: {e}")
        return None


def update_kategori(id, data, user_id):
    """Memperbarui kategori berdasarkan ID."""
    try:
        kategori = Kategori.query.filter_by(id=id, user_id=user_id).first()
        if not kategori:
            return None

        # Update hanya field yang benar-benar dikirim.
        if "nama" in data:
            kategori.nama = data["nama"]
        if "tipe" in data:
            kategori.tipe = data["tipe"]

        db.session.commit()
        return {
            "id": kategori.id,
            "nama": kategori.nama,
            "tipe": kategori.tipe,
            "created_at": kategori.created_at,
        }
    except Exception as e:
        db.session.rollback()
        print(f"Error updating category: {e}")
        return None


def delete_kategori(id, user_id):
    """Menghapus kategori berdasarkan ID."""
    try:
        kategori = Kategori.query.filter_by(id=id, user_id=user_id).first()
        if not kategori:
            return False

        db.session.delete(kategori)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting category: {e}")
        return False


