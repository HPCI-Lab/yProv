from flask import Blueprint, jsonify, request

from prov.model import ProvDocument
from py2neo.data import Node
from py2neo.matching import NodeMatcher

from extension import neo4j
from utils import node_to_json, json_element_to_prov_element, prov_element_to_node


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
'''
al momento ancora difetta:
- puo aggiungere altri elementi
- non aggiunge prefissi passati in request.json
- non gestisce errori
- non fa check se entita esiste ancora
'''
@entities_bp.route('', methods=['POST'])
def create_entities(doc_id):

    prov_document = ProvDocument()
    graph_db = neo4j.get_db(doc_id)

    # get the ns of the document
    for ns in graph_db.call.n10s.nsprefixes.list():
        prov_document.add_namespace(ns[0], ns[1])

    # parsing
    prov_element = json_element_to_prov_element(request.json, prov_document)
    node = prov_element_to_node(prov_element)

    # save in the graph
    graph_db.create(node)


    '''
    # cicla su input dict 
    for rec_type_str in request.json:
        
        # get the type of the record 
        rec_type = PROV_RECORD_IDS_MAP[rec_type_str]

        for rec_id, content in request.json[rec_type_str].items():
            if hasattr(content, "items"):  # it is a dict
                #  There is only one element, create a singleton list
                elements = [content]
            else:
                # expect it to be a list of dictionaries
                elements = content
        print(elements)

    node = json_to_node(request.json)

    # save in the graph
    graph_db.create(node)
    '''
    return "New entity created", 201