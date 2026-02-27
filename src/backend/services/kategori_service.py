
from models.kategori import Kategori
from config import db

def get_kategori():
    """Get all categories"""
    try:
        kategori = Kategori.query.all()
        return [{'id': k.id, 'nama': k.nama, 'tipe': k.tipe, 'created_at': k.created_at} for k in kategori]
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []

def create_kategori(data):
    """Create a new category"""
    try:
        new_kategori = Kategori(nama=data['nama'], tipe=data['tipe'])
        db.session.add(new_kategori)
        db.session.commit()
        return {'id': new_kategori.id, 'nama': new_kategori.nama, 'tipe': new_kategori.tipe, 'created_at': new_kategori.created_at}
    except Exception as e:
        db.session.rollback()
        print(f"Error creating category: {e}")
        return None

def update_kategori(id, data):
    """Update an existing category"""
    try:
        kategori = Kategori.query.get(id)
        if not kategori:
            return None
        if 'nama' in data:
            kategori.nama = data['nama']
        if 'tipe' in data:
            kategori.tipe = data['tipe']
        db.session.commit()
        return {'id': kategori.id, 'nama': kategori.nama, 'tipe': kategori.tipe, 'created_at': kategori.created_at}
    except Exception as e:
        db.session.rollback()
        print(f"Error updating category: {e}")
        return None

def delete_kategori(id):
    """Delete a category"""
    try:
        kategori = Kategori.query.get(id)
        if not kategori:
            return False
        db.session.delete(kategori)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting category: {e}")
        return False

