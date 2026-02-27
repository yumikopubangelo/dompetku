
from config import db
from datetime import datetime

class Kategori(db.Model):
    __tablename__ = 'kategori'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100), nullable=False)
    tipe = db.Column(db.Enum('pemasukan', 'pengeluaran'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Kategori {self.nama}>"

