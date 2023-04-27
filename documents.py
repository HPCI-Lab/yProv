from flask import Blueprint, jsonify, request
documents_bp = Blueprint('documents', __name__)

# Get a document
@documents_bp.route('/<string:doc_id>/', methods=['GET'])
def get_document(doc_id):
    # turn the JSON output into a Response object with application/json mime-type
    return jsonify({'name': doc_id})


# Create a document
@documents_bp.route('/<string:doc_id>/', methods=['PUT'])
def create_document(doc_id):
    print(request.json)
    return "Ok"