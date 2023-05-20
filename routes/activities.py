from flask import Blueprint, jsonify, request
from py2neo import Node
from py2neo.matching import NodeMatcher

from extension import neo4j
from .utils import node_to_json, json_to_node

activities_bp = Blueprint('activities', __name__)


# Get an activity
@activities_bp.route('/<string:ag_id>', methods=['GET'])
def get_activity(doc_id, ac_id):
    # get the graph db
    graph_db = neo4j.get_db(doc_id)
    # match the node
    nodes = NodeMatcher(graph_db)
    node = nodes.match('Activity', id=ac_id).first() 
    # otherwise with evaluate and Cypher

    return jsonify(node_to_json(node, 'activity'))


# Create an activity
@activities_bp.route('', methods=['POST'])
def create_activity(doc_id):

    node = json_to_node(request.json)

    # save in the graph
    graph_db = neo4j.get_db(doc_id)
    graph_db.create(node)
    
    return "New activity created", 201