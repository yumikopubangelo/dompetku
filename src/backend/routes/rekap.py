"""Route API untuk fitur rekap bulanan."""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.rekap_service import get_rekap_bulanan

# Blueprint rekap, akan di-mount dengan prefix `/api/rekap`.
rekap_bp = Blueprint("rekap", __name__)


@rekap_bp.route("/bulanan", methods=["GET"])
@jwt_required()
def get_rekap_bulanan_route():
    """Mengambil ringkasan pemasukan/pengeluaran berdasarkan bulan dan tahun."""
    # Ambil parameter query string.
    bulan = request.args.get("bulan", None)
    tahun = request.args.get("tahun", None)

    # Keduanya wajib ada agar rekap terhitung untuk periode spesifik.
    if not bulan or not tahun:
        return jsonify({"error": "Parameter bulan dan tahun wajib disediakan"}), 400

    try:
        # Konversi parameter ke integer sebelum diproses service.
        rekap = get_rekap_bulanan(int(bulan), int(tahun))
        return jsonify(rekap), 200
    except Exception as e:
        # Error runtime dikembalikan sebagai respons 500.
        return jsonify({"error": str(e)}), 500

