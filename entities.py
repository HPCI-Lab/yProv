from flask import Blueprint, jsonify, request
entities_bp = Blueprint('entities', __name__)

from py2neo import Node


from neo4jconnector import Client
client = Client()


# Get an entity
@entities_bp.route('/<string:e_id>/', methods=['GET'])
def get_entities(doc_id, e_id):

    return jsonify({'doc_id': doc_id, 'e_id': e_id})


# Create an entity
@entities_bp.route('/', methods=['POST'])
def create_entities(doc_id):

    element = request.json

    # get label, id and props of the element
    node_label = list(element.keys())[0]
    node_id = list(element[node_label].keys())[0]
    node_props = element[node_label][node_id]

    # create a node instance    
    node = Node(node_label.capitalize(), id=node_id, **node_props)

    # save in the graph
    graph_db = client.get_db(doc_id)
    tx = graph_db.begin()
    tx.create(node)
    tx.commit()
    
    return "New entity created", 201