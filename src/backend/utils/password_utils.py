"""Utilitas keamanan password untuk proses autentikasi."""

from werkzeug.security import check_password_hash, generate_password_hash


def hash_password(plain_password):
    """Mengubah password plaintext menjadi hash satu arah yang aman disimpan."""
    if plain_password is None or str(plain_password).strip() == "":
        raise ValueError("Password tidak boleh kosong")

    return generate_password_hash(plain_password, method="pbkdf2:sha256", salt_length=16)


def verify_password(plain_password, hashed_password):
    """Memverifikasi apakah password plaintext cocok dengan hash yang tersimpan."""
    if not hashed_password:
        return False

    if plain_password is None:
        return False

    return check_password_hash(hashed_password, plain_password)


def decrypt_password(plain_password, hashed_password):
    """Alias kompatibilitas.

    Catatan:
    Hash password tidak bisa didekripsi. Untuk kasus autentikasi,
    yang benar adalah melakukan verifikasi kecocokan password.
    """
    return verify_password(plain_password, hashed_password)
