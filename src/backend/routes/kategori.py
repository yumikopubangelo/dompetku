
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.kategori_service import get_kategori, create_kategori, update_kategori, delete_kategori

kategori_bp = Blueprint('kategori', __name__)

@kategori_bp.route('/', methods=['GET'])
@jwt_required()
def get_kategori_route():
    return jsonify(get_kategori()), 200

@kategori_bp.route('/', methods=['POST'])
@jwt_required()
def create_kategori_route():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    kategori = create_kategori(data)
    return jsonify(kategori), 201

@kategori_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_kategori_route(id):
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    kategori = update_kategori(id, data)
    if kategori:
        return jsonify(kategori), 200
    return jsonify({'error': 'Kategori not found'}), 404

@kategori_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_kategori_route(id):
    success = delete_kategori(id)
    if success:
        return jsonify({'message': 'Kategori deleted successfully'}), 200
    return jsonify({'error': 'Kategori not found'}), 404

