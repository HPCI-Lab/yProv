from flask import Blueprint, request
import click
from prov.model import ProvDocument
from py2neo.matching import NodeMatcher
import json,sys
from extensions import neo4j

from .utils import (
    NS_NODE_LABEL,
    json_to_prov_record,
    prov_element_to_node,
    node_to_prov_element,
    prov_element_to_json,
    set_document_ns               
)


entities_bp = Blueprint('entities', __name__)

# Create
@entities_bp.cli.command('create')
@click.argument("doc_id")
@click.argument("file", type=click.Path(exists=True))
def create_entity(doc_id,file):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        print("DB error")
        sys.exit()

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        print("Document not found")
        sys.exit()   

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    # parsing
    with open(file,"r") as fp:
        data = json.load(fp)

    #prov_element = json_to_prov_record(request.json, prov_document)
    prov_element = json_to_prov_record(data, prov_document)
    node = prov_element_to_node(prov_element)

    try:
        graph.create(node)
    except:
        print("DB error")
        sys.exit()

    print("Element created")

# Read
#@entities_bp.route('/<string:e_id>', methods=['GET'])
@entities_bp.cli.command('get')
@click.argument("doc_id")
@click.argument("e_id")
def get_entity(doc_id, e_id):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        print("DB error")
        sys.exit()

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        print("Document not found")
        sys.exit()

    # check if element is in document 
    try:
        # match the node
        node_matcher = NodeMatcher(graph)
        node = node_matcher.match('Entity', id=e_id).first() 
        assert(node)
    except AssertionError:
        print("Entity not found")
        sys.exit()
    
    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    prov_element = node_to_prov_element(node, prov_document)

    print(prov_element_to_json(prov_element))

# Update
@entities_bp.cli.command('update')
@click.argument("doc_id")
@click.argument("e_id")
@click.argument("file")
def replace_entity(doc_id, e_id,file):
    try:
        graph = neo4j.get_db(doc_id)
    except:
       print("DB error")
       sys.exit()

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        print("Document not found")
        sys.exit()

    # match the node
    node_matcher = NodeMatcher(graph)
    node = node_matcher.match('Entity', id=e_id).first() 
    # node = node_matcher.match(id=e_id).first()

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    # parsing
    with open(file,"r") as fp:
        data = json.load(fp)

    prov_element = json_to_prov_record(data, prov_document)
    input_node = prov_element_to_node(prov_element)
    
    # if exist then update else create
    if(node):
        node.clear()
        for key, value in input_node.items():
            node[key]=value

        graph.push(node)

        print("Entity updated")
    else:
        try:
            graph.create(input_node)
        except:
            print("DB error")
            sys.exit()
        
        print("Entity created")

# Delete
@entities_bp.cli.command('delete')
@click.argument("doc_id")
@click.argument("e_id")
def delete_entity(doc_id, e_id):
    try:
        graph = neo4j.get_db(doc_id)
    except:
        print("DB error")
        sys.exit()

    # check if document is in neo4j 
    try:
        assert graph
    except AssertionError:
        print("Document not found")
        sys.exit()

    # check if element is in document 
    try:
        # match the node
        node_matcher = NodeMatcher(graph)
        node = node_matcher.match('Entity', id=e_id).first() 
        # node = node_matcher.match(id=e_id).first()
        assert(node)
    except AssertionError:
        print("Element not found")
        sys.exit()
    
    try:
        graph.delete(node)
    except AssertionError:
        print("DB error")
        sys.exit()

    print("Element deleted")
