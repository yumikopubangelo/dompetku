"""Route API untuk fitur pengeluaran."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.pengeluaran_service import get_pengeluaran, create_pengeluaran, update_pengeluaran, delete_pengeluaran

# Blueprint pengeluaran, akan di-mount dengan prefix `/api/pengeluaran`.
pengeluaran_bp = Blueprint("pengeluaran", __name__)


@pengeluaran_bp.route("/", methods=["GET"])
@jwt_required()
def get_pengeluaran_route():
    """Mengambil seluruh transaksi pengeluaran."""
    user_id = get_jwt_identity()
    return jsonify(get_pengeluaran(user_id)), 200


@pengeluaran_bp.route("/", methods=["POST"])
@jwt_required()
def create_pengeluaran_route():
    """Membuat transaksi pengeluaran baru."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user_id = get_jwt_identity()
    pengeluaran = create_pengeluaran(data, user_id)
    return jsonify(pengeluaran), 201


@pengeluaran_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_pengeluaran_route(id):
    """Memperbarui transaksi pengeluaran berdasarkan ID."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    user_id = get_jwt_identity()
    pengeluaran = update_pengeluaran(id, data, user_id)
    if pengeluaran:
        return jsonify(pengeluaran), 200

    return jsonify({"error": "Pengeluaran not found"}), 404


@pengeluaran_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_pengeluaran_route(id):
    """Menghapus transaksi pengeluaran berdasarkan ID."""
    user_id = get_jwt_identity()
    success = delete_pengeluaran(id, user_id)
    if success:
        return jsonify({"message": "Pengeluaran deleted successfully"}), 200

    return jsonify({"error": "Pengeluaran not found"}), 404

