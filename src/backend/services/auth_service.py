"""Business logic untuk fitur autentikasi login/logout."""

from flask_jwt_extended import create_access_token, create_refresh_token

from models.user import User

from utils.password_utils import verify_password, hash_password
from config import db


# Token blacklist in-memory.
# Cocok untuk development; untuk production sebaiknya disimpan di Redis/DB.
REVOKED_TOKEN_JTI = set()


def authenticate_user(username, plain_password):
    """Memvalidasi kredensial user berdasarkan username dan password."""
    user = User.query.filter_by(username=username).first()
    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(plain_password, user.password_hash):
        return None

    return user


def generate_auth_tokens(user):
    """Membuat access token dan refresh token untuk user yang valid."""
    additional_claims = {"username": user.username}
    identity = str(user.id)

    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)

    return {"access_token": access_token, "refresh_token": refresh_token}


def revoke_token(jti):
    """Menandai token JWT sebagai revoked (logout)."""
    REVOKED_TOKEN_JTI.add(jti)


def is_token_revoked(jti):
    """Mengecek apakah token JWT sudah masuk daftar revoke."""
    return jti in REVOKED_TOKEN_JTI


def register_new_user(username, password):
    """Membuat user baru dengan username dan password yang diberikan."""
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise ValueError("Username sudah digunakan")

    password_hash = hash_password(password)
    new_user = User(username=username, password_hash=password_hash, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return new_user
