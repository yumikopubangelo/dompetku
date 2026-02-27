from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.rekap_service import get_rekap_bulanan

rekap_bp = Blueprint('rekap', __name__)

@rekap_bp.route('/bulanan', methods=['GET'])
@jwt_required()
def get_rekap_bulanan_route():
    # Ambil parameter bulan dan tahun dari query string
    bulan = request.args.get('bulan', None)
    tahun = request.args.get('tahun', None)
    
    if not bulan or not tahun:
        return jsonify({'error': 'Parameter bulan dan tahun wajib disediakan'}), 400
    
    try:
        rekap = get_rekap_bulanan(int(bulan), int(tahun))
        return jsonify(rekap), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
