"""Route API untuk fitur saldo akhir."""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.saldo_service import get_saldo_akhir

# Blueprint saldo, akan di-mount dengan prefix `/api/saldo`.
saldo_bp = Blueprint("saldo", __name__)


@saldo_bp.route("/", methods=["GET"])
@jwt_required()
def get_saldo_akhir_route():
    """Mengambil saldo akhir berdasarkan total pemasukan dikurangi pengeluaran."""
    try:
        user_id = get_jwt_identity()
        saldo = get_saldo_akhir(user_id)
        # Nilai saldo diubah ke string agar serialisasi desimal konsisten.
        return jsonify({"saldo_akhir": str(saldo)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

