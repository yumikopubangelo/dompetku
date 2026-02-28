"""Route API untuk fitur statistik keuangan."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.statistik_service import get_statistik_keuangan

# Blueprint statistik, akan di-mount dengan prefix `/api/statistik`.
statistik_bp = Blueprint("statistik", __name__)


@statistik_bp.route("/", methods=["GET"])
@jwt_required()
def get_statistik_keuangan_route():
    """Mengambil statistik tahunan, default ke tahun berjalan."""
    # Parameter tahun bersifat opsional.
    tahun = request.args.get("tahun", None)

    try:
        # Jika tahun dikirim, konversi dulu ke integer.
        if tahun:
            tahun = int(tahun)

        statistik = get_statistik_keuangan(tahun)
        return jsonify(statistik), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

