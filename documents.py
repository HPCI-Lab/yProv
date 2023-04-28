from flask import Blueprint, jsonify, request

from extension import neo4j

documents_bp = Blueprint('documents', __name__)

# Get a document
@documents_bp.route('/<string:doc_id>', methods=['GET'])
def get_document(doc_id):


    return jsonify({'name': doc_id})


# Create a document
@documents_bp.route('/<string:doc_id>', methods=['PUT'])
def create_document(doc_id):
    # get the db instance
    # if not there yet create it  
    graph_db = neo4j.get_db(doc_id)

    if(graph_db==None):
        graph_db = neo4j.create_db(doc_id)

        return "Document created", 201
    
    else:
        return "Document already exists", 400    