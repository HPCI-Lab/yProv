from flask import Blueprint, request

from prov.model import ProvDocument
from py2neo.matching import NodeMatcher
from py2neo import Node

from extension import neo4j
from utils import json_to_prov_record, prov_element_to_node, node_to_prov_element, prov_element_to_json


entities_bp = Blueprint('entities', __name__)

# Create
'''
    Idempotente, non faccio check se esiste già entità
'''
@entities_bp.route('', methods=['POST'])
def create_entities(doc_id):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        return "DB error", 500

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        return "Document not found", 404

    prov_document = ProvDocument()

    # get the ns of the document
    for ns in graph.call.n10s.nsprefixes.list():
        prov_document.add_namespace(ns[0], ns[1])

    # parsing
    prov_element = json_to_prov_record(request.json, prov_document)
    node = prov_element_to_node(prov_element)

    try:
        graph.create(node)
    except:
        return "DB error", 500

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
    graph.create(node)
    '''
    return "New entity created", 201

# Read
@entities_bp.route('/<string:e_id>', methods=['GET'])
def get_entities(doc_id, e_id):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        return "DB error", 500

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        return "Document not found", 404

    # check if element is in document 
    try:
        # match the node
        node_matcher = NodeMatcher(graph)
        # node = node_matcher.match('Entity', id=e_id).first() 
        node = node_matcher.match(id=e_id).first()
        assert(node)
    except AssertionError:
        return "Element not found", 404
    

    prov_document = ProvDocument()
    # get the ns of the document
    for ns in graph.call.n10s.nsprefixes.list():
        prov_document.add_namespace(ns[0], ns[1])

    prov_element = node_to_prov_element(node, prov_document)

    return prov_element_to_json(prov_element)

# Update
@entities_bp.route('/<string:e_id>', methods=['PUT'])
def replace_entities(doc_id, e_id):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        return "DB error", 500

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        return "Document not found", 404

    # match the node
    node_matcher = NodeMatcher(graph)
    # node = node_matcher.match('Entity', id=e_id).first() 
    node = node_matcher.match(id=e_id).first()


    prov_document = ProvDocument()

    # get the ns of the document
    for ns in graph.call.n10s.nsprefixes.list():
        prov_document.add_namespace(ns[0], ns[1])

    # parsing
    prov_element = json_to_prov_record(request.json, prov_document)
    input_node = prov_element_to_node(prov_element)
    
    # if exist then update else create
    if(node):
        node.clear()
        for key, value in input_node.items():
            node[key]=value

        transaction = graph.begin()
        transaction.graph.push(node)
        transaction.commit()

        return "Element updated", 200
    else:
        try:
            graph.create(input_node)
        except:
            return "DB error", 500
        
        return "Element created", 201

# Delete
@entities_bp.route('/<string:e_id>', methods=['DELETE'])
def delete_entities(doc_id, e_id):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        return "DB error", 500

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        return "Document not found", 404

    # check if element is in document 
    try:
        # match the node
        node_matcher = NodeMatcher(graph)
        # node = node_matcher.match('Entity', id=e_id).first() 
        node = node_matcher.match(id=e_id).first()
        assert(node)
    except AssertionError:
        return "Element not found", 404
    
    try:
        graph.delete(node)
    except AssertionError:
        return "DB error", 500

    return "Element deleted", 200