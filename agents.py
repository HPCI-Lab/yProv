from flask import Blueprint, jsonify, request
from py2neo import Node
from py2neo.matching import NodeMatcher

from extension import neo4j
from elements import node_to_json, json_to_node

agents_bp = Blueprint('agents', __name__)


# Get an agent
@agents_bp.route('/<string:ag_id>', methods=['GET'])
def get_agents(doc_id, ag_id):
    # get the graph db
    graph_db = neo4j.get_db(doc_id)
    # match the node
    nodes = NodeMatcher(graph_db)
    node = nodes.match('Agent', id=ag_id).first() 
    # otherwise with evaluate and Cypher

    return jsonify(node_to_json(node, 'agent'))


# Create an agent
@agents_bp.route('', methods=['POST'])
def create_agents(doc_id):

    node = json_to_node(request.json)

    # save in the graph
    graph_db = neo4j.get_db(doc_id)
    graph_db.create(node)
    
    return "New agent created", 201