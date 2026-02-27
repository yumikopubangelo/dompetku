from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from services.saldo_service import get_saldo_akhir

saldo_bp = Blueprint('saldo', __name__)

@saldo_bp.route('/', methods=['GET'])
@jwt_required()
def get_saldo_akhir_route():
    try:
        saldo = get_saldo_akhir()
        return jsonify({'saldo_akhir': str(saldo)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
