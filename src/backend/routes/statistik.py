from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.statistik_service import get_statistik_keuangan

statistik_bp = Blueprint('statistik', __name__)

@statistik_bp.route('/', methods=['GET'])
@jwt_required()
def get_statistik_keuangan_route():
    # Ambil parameter tahun dari query string (default: tahun sekarang)
    tahun = request.args.get('tahun', None)
    
    try:
        if tahun:
            tahun = int(tahun)
        statistik = get_statistik_keuangan(tahun)
        return jsonify(statistik), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
