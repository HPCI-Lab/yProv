from flask import Blueprint, jsonify, request
from py2neo import Node
from py2neo.matching import NodeMatcher
from neo4jconnector import Client


entities_bp = Blueprint('entities', __name__)
client = Client()


# Get an entity
@entities_bp.route('/<string:e_id>/', methods=['GET'])
def get_entities(doc_id, e_id):
    # get the graph db
    graph_db = client.get_db(doc_id)
    # match the node
    nodes = NodeMatcher(graph_db)
    node = nodes.match("Entity", id=e_id).first() 
    # otherwise evaluate with Cypher

    # construct the return JSON
    element_id = ""
    element_props = {}
    for key in node.keys():
        if(key=='id'):
            element_id = node[key]
        else:
            element_props[key] = node[key]

    element = {
        "entity" : {
            element_id : element_props
        }
    }

    return jsonify(element)


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
    '''
    tx = graph_db.begin()
    tx.create(node)
    tx.commit() # deprecated
    '''
    # print(graph_db.exists(node)) # output False
    graph_db.create(node)
    
    return "New entity created", 201