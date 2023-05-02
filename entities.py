from flask import Blueprint, jsonify, request
from py2neo import Node
from py2neo.matching import NodeMatcher

from extension import neo4j
from elements import node_to_json, json_to_node

entities_bp = Blueprint('entities', __name__)


# Get an entity
@entities_bp.route('/<string:e_id>', methods=['GET'])
def get_entities(doc_id, e_id):
    # get the graph db
    graph_db = neo4j.get_db(doc_id)
    # match the node
    nodes = NodeMatcher(graph_db)
    node = nodes.match('Entity', id=e_id).first() 
    # otherwise with evaluate and Cypher

    return jsonify(node_to_json(node, 'entity'))


# Create an entity
@entities_bp.route('', methods=['POST'])
def create_entities(doc_id):

    node = json_to_node(request.json)

    # save in the graph
    graph_db = neo4j.get_db(doc_id)
    graph_db.create(node)
    
    return "New entity created", 201