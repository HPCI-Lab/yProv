from flask import Blueprint, jsonify, request
entities_bp = Blueprint('entities', __name__)

# Get an entity
@entities_bp.route('/<string:e_id>/', methods=['GET'])
def get_document(doc_id, e_id):

    return jsonify({'doc_id': doc_id, 'e_id': e_id})


# Create an entiey
@entities_bp.route('/', methods=['POST'])
def create_document(doc_id):
    entity = request.json["entity"]
    print(entity)

    return "Ok"