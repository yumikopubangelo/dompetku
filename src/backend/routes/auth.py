"""Route API untuk autentikasi user (login/logout)."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from services.auth_service import authenticate_user, generate_auth_tokens, revoke_token, create_user

# Blueprint auth, akan di-mount dengan prefix `/api/auth`.
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_route():
    """Registrasi user baru."""
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    email = data.get("email", "")

    if not username or not password:
        return jsonify({"error": "username dan password wajib diisi"}), 400

    if len(password) < 6:
        return jsonify({"error": "password minimal 6 karakter"}), 400

    user, error = create_user(username, password, email)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(
        {
            "message": "Registrasi berhasil",
            "user": {"id": user.id, "username": user.username},
        }
    ), 201


@auth_bp.route("/login", methods=["POST"])
def login_route():
    """Login user dengan username dan password."""
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username dan password wajib diisi"}), 400

    user = authenticate_user(username, password)
    if not user:
        return jsonify({"error": "username atau password salah"}), 401

    tokens = generate_auth_tokens(user)
    return jsonify(
        {
            "message": "Login berhasil",
            "user": {"id": user.id, "username": user.username},
            **tokens,
        }
    ), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout_route():
    """Logout user dengan me-revoke token yang sedang dipakai."""
    jti = get_jwt()["jti"]
    revoke_token(jti)
    return jsonify({"message": "Logout berhasil"}), 200
