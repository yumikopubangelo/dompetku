from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.pengeluaran_service import get_pengeluaran, create_pengeluaran, update_pengeluaran, delete_pengeluaran

pengeluaran_bp = Blueprint('pengeluaran', __name__)

@pengeluaran_bp.route('/', methods=['GET'])
@jwt_required()
def get_pengeluaran_route():
    return jsonify(get_pengeluaran()), 200

@pengeluaran_bp.route('/', methods=['POST'])
@jwt_required()
def create_pengeluaran_route():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    pengeluaran = create_pengeluaran(data)
    return jsonify(pengeluaran), 201

@pengeluaran_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_pengeluaran_route(id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    pengeluaran = update_pengeluaran(id, data)
    if pengeluaran:
        return jsonify(pengeluaran), 200
    return jsonify({'error': 'Pengeluaran not found'}), 404

@pengeluaran_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_pengeluaran_route(id):
    success = delete_pengeluaran(id)
    if success:
        return jsonify({'message': 'Pengeluaran deleted successfully'}), 200
    return jsonify({'error': 'Pengeluaran not found'}), 404
