<<<<<<< HEAD
# Business logic untuk fitur Pemasukan
=======
from models.pemasukan import Pemasukan
from config import db

def get_pemasukan():
    """Get all income records"""
    try:
        pemasukan = Pemasukan.query.all()
        return [{'id': p.id, 'jumlah': str(p.jumlah), 'deskripsi': p.deskripsi, 'kategori_id': p.kategori_id, 'tanggal': p.tanggal, 'created_at': p.created_at} for p in pemasukan]
    except Exception as e:
        print(f"Error getting income: {e}")
        return []

def create_pemasukan(data):
    """Create a new income record"""
    try:
        new_pemasukan = Pemasukan(
            jumlah=data['jumlah'],
            deskripsi=data.get('deskripsi'),
            kategori_id=data.get('kategori_id'),
            tanggal=data['tanggal']
        )
        db.session.add(new_pemasukan)
        db.session.commit()
        return {'id': new_pemasukan.id, 'jumlah': str(new_pemasukan.jumlah), 'deskripsi': new_pemasukan.deskripsi, 'kategori_id': new_pemasukan.kategori_id, 'tanggal': new_pemasukan.tanggal, 'created_at': new_pemasukan.created_at}
    except Exception as e:
        db.session.rollback()
        print(f"Error creating income: {e}")
        return None

def update_pemasukan(id, data):
    """Update an existing income record"""
    try:
        pemasukan = Pemasukan.query.get(id)
        if not pemasukan:
            return None
        if 'jumlah' in data:
            pemasukan.jumlah = data['jumlah']
        if 'deskripsi' in data:
            pemasukan.deskripsi = data['deskripsi']
        if 'kategori_id' in data:
            pemasukan.kategori_id = data['kategori_id']
        if 'tanggal' in data:
            pemasukan.tanggal = data['tanggal']
        db.session.commit()
        return {'id': pemasukan.id, 'jumlah': str(pemasukan.jumlah), 'deskripsi': pemasukan.deskripsi, 'kategori_id': pemasukan.kategori_id, 'tanggal': pemasukan.tanggal, 'created_at': pemasukan.created_at}
    except Exception as e:
        db.session.rollback()
        print(f"Error updating income: {e}")
        return None

def delete_pemasukan(id):
    """Delete an income record"""
    try:
        pemasukan = Pemasukan.query.get(id)
        if not pemasukan:
            return False
        db.session.delete(pemasukan)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting income: {e}")
        return False
>>>>>>> 4631ec9 (chore: initialize project structure with src, tests, docs, and configuration)
