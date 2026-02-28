"""Route API untuk fitur pemasukan."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.pemasukan_service import get_pemasukan, create_pemasukan, update_pemasukan, delete_pemasukan

# Blueprint pemasukan, akan di-mount dengan prefix `/api/pemasukan`.
pemasukan_bp = Blueprint("pemasukan", __name__)


@pemasukan_bp.route("/", methods=["GET"])
@jwt_required()
def get_pemasukan_route():
    """Mengambil seluruh transaksi pemasukan."""
    return jsonify(get_pemasukan()), 200


@pemasukan_bp.route("/", methods=["POST"])
@jwt_required()
def create_pemasukan_route():
    """Membuat transaksi pemasukan baru."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    pemasukan = create_pemasukan(data)
    return jsonify(pemasukan), 201


@pemasukan_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_pemasukan_route(id):
    """Memperbarui transaksi pemasukan berdasarkan ID."""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    pemasukan = update_pemasukan(id, data)
    if pemasukan:
        return jsonify(pemasukan), 200

    return jsonify({"error": "Pemasukan not found"}), 404


@pemasukan_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_pemasukan_route(id):
    """Menghapus transaksi pemasukan berdasarkan ID."""
    success = delete_pemasukan(id)
    if success:
        return jsonify({"message": "Pemasukan deleted successfully"}), 200

    return jsonify({"error": "Pemasukan not found"}), 404

