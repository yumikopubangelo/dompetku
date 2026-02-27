from config import db
from datetime import datetime

class Pemasukan(db.Model):
    __tablename__ = 'pemasukan'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jumlah = db.Column(db.Numeric(15, 2), nullable=False)
    deskripsi = db.Column(db.Text)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.id'))
    tanggal = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    kategori = db.relationship('Kategori', backref=db.backref('pemasukan', lazy=True))
    
    def __repr__(self):
        return f"<Pemasukan {self.jumlah}>"
