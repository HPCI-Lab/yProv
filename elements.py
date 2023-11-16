from flask import Blueprint, request

from prov.model import ProvDocument
from py2neo.matching import NodeMatcher

from extensions import neo4j

from .utils import (
    NS_NODE_LABEL,
    json_to_prov_record,
    prov_element_to_node,
    node_to_prov_element,
    prov_element_to_json,
    set_document_ns               
)


elements_bp = Blueprint('elements', __name__)

# Create
#@elements_bp.route('', methods=['POST'])
@elements_bp.cli.command('create')
@click.argument("doc_id")
@click.argument("input_file")
def create_element(doc_id,input_file):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        #return "DB error", 500
        print("DB error")

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        #return "Document not found", 404
        print("Document not found")

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    # parsing
    import json
    f = open(input_file)
    data = json.load(f)
    #prov_element = json_to_prov_record(request.json, prov_document)
    prov_element = json_to_prov_record(data, prov_document)
    node = prov_element_to_node(prov_element)

    try:
        graph.create(node)
    except:
        #return "DB error", 500
        print("DB error")

    #return "Element created", 201
    print("Element created")

# Read
#@elements_bp.route('/<string:e_id>', methods=['GET'])
@elements_bp.cli.command('get')
@click.argument("doc_id")
@click.argument("e_id")
def get_element(doc_id, e_id):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        #return "DB error", 500
        print("DB error")

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        #return "Document not found", 404
        print("Document not found")

    # check if element is in document 
    try:
        # match the node
        node_matcher = NodeMatcher(graph)
        node = node_matcher.match(id=e_id).first() 
        assert(node)
    except AssertionError:
        #return "Element not found", 404
        print("Element not found")
    

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    prov_element = node_to_prov_element(node, prov_document)

    #return prov_element_to_json(prov_element)
    print(prov_element_to_json(prov_element))

# Update
#@elements_bp.route('/<string:e_id>', methods=['PUT'])
@elements_bp.cli.command('update')
@click.argument("doc_id")
@click.argument("e_id")
@click.argument("input_file")
def replace_element(doc_id, e_id,input_file):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        #return "DB error", 500
        print("DB error")

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        #return "Document not found", 404
        print("Document not found")

    # match the node
    node_matcher = NodeMatcher(graph)
    # node = node_matcher.match('Entity', id=e_id).first() 
    node = node_matcher.match(id=e_id).first()

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    # parsing
    import json
    f = open(input_file)
    data = json.load(f)
    #prov_element = json_to_prov_record(request.json, prov_document)
    prov_element = json_to_prov_record(data, prov_document)
    input_node = prov_element_to_node(prov_element)
    
    # if exist then update else create
    if(node):
        node.clear()
        for key, value in input_node.items():
            node[key]=value

        graph.push(node)

        #return "Element updated", 200
        print("Element updated")
    else:
        try:
            graph.create(input_node)
        except:
            #return "DB error", 500
            print("DB error")
        
        #return "Element created", 201
        print("Element created")

# Delete
#@elements_bp.route('/<string:e_id>', methods=['DELETE'])
@elements_bp.cli.command('delete')
@click.argument("doc_id")
@click.argument("e_id")
def delete_element(doc_id, e_id):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        #return "DB error", 500
        print("DB error")

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        #return "Document not found", 404
        print("Document not found")

    # check if element is in document 
    try:
        # match the node
        node_matcher = NodeMatcher(graph)
        # node = node_matcher.match('Entity', id=e_id).first() 
        node = node_matcher.match(id=e_id).first()
        assert(node)
    except AssertionError:
        #return "Element not found", 404
        print("Element not found")
    
    try:
        graph.delete(node)
    except AssertionError:
        #return "DB error", 500
        print("DB error")

    #return "Element deleted", 200
    print("Element deleted")