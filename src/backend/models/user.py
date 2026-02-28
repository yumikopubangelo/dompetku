"""Model user untuk autentikasi login/logout."""

from datetime import datetime

from config import db


class User(db.Model):
    """Representasi akun user aplikasi."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """Representasi ringkas user untuk kebutuhan debugging."""
        return f"<User {self.username}>"
