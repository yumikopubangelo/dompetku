from models.pengeluaran import Pengeluaran
from config import db

def get_pengeluaran():
    """Get all expense records"""
    try:
        pengeluaran = Pengeluaran.query.all()
        return [{'id': p.id, 'jumlah': str(p.jumlah), 'deskripsi': p.deskripsi, 'kategori_id': p.kategori_id, 'tanggal': p.tanggal, 'created_at': p.created_at} for p in pengeluaran]
    except Exception as e:
        print(f"Error getting expenses: {e}")
        return []

def create_pengeluaran(data):
    """Create a new expense record"""
    try:
        new_pengeluaran = Pengeluaran(
            jumlah=data['jumlah'],
            deskripsi=data.get('deskripsi'),
            kategori_id=data.get('kategori_id'),
            tanggal=data['tanggal']
        )
        db.session.add(new_pengeluaran)
        db.session.commit()
        return {'id': new_pengeluaran.id, 'jumlah': str(new_pengeluaran.jumlah), 'deskripsi': new_pengeluaran.deskripsi, 'kategori_id': new_pengeluaran.kategori_id, 'tanggal': new_pengeluaran.tanggal, 'created_at': new_pengeluaran.created_at}
    except Exception as e:
        db.session.rollback()
        print(f"Error creating expense: {e}")
        return None

def update_pengeluaran(id, data):
    """Update an existing expense record"""
    try:
        pengeluaran = Pengeluaran.query.get(id)
        if not pengeluaran:
            return None
        if 'jumlah' in data:
            pengeluaran.jumlah = data['jumlah']
        if 'deskripsi' in data:
            pengeluaran.deskripsi = data['deskripsi']
        if 'kategori_id' in data:
            pengeluaran.kategori_id = data['kategori_id']
        if 'tanggal' in data:
            pengeluaran.tanggal = data['tanggal']
        db.session.commit()
        return {'id': pengeluaran.id, 'jumlah': str(pengeluaran.jumlah), 'deskripsi': pengeluaran.deskripsi, 'kategori_id': pengeluaran.kategori_id, 'tanggal': pengeluaran.tanggal, 'created_at': pengeluaran.created_at}
    except Exception as e:
        db.session.rollback()
        print(f"Error updating expense: {e}")
        return None

def delete_pengeluaran(id):
    """Delete an expense record"""
    try:
        pengeluaran = Pengeluaran.query.get(id)
        if not pengeluaran:
            return False
        db.session.delete(pengeluaran)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting expense: {e}")
        return False
