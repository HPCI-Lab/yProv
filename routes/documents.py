import json
import os

import click
from flask import request, Response, Blueprint
from prov.model import ProvDocument, ProvElement, ProvRelation
from prov.graph import INFERRED_ELEMENT_CLASS
from py2neo.data import Subgraph, Node
from py2neo.matching import NodeMatcher, RelationshipMatcher
# from prov2neo.encode import encode_graph

from extensions import neo4j
from .utils import (
    ELEMENT_NODE_PRIMARY_LABEL,
    ELEMENT_NODE_PRIMARY_ID,
    NS_NODE_LABEL,
    prov_element_to_node, 
    prov_relation_to_edge,
    node_to_prov_element,
    edge_to_prov_relation,
    get_ns_node,
    set_document_ns
)

documents_bp = Blueprint('documents', __name__)


def prov_to_graph(prov_document):

    graph = Subgraph()
    # Returns a new document containing all records having same identifiers unified (including those inside bundles)
    unified = prov_document.unified()
    node_map = dict()

    for element in unified.get_records(ProvElement):
        node = prov_element_to_node(element)
        graph = graph | node        # union operator: add Node to the Subgraph
        node_map[element.identifier] = node

    for relation in unified.get_records(ProvRelation):
        # taking the first two elements of a relation
        attr_pair_1, attr_pair_2 = relation.formal_attributes[:2]
        # only need the QualifiedName (i.e. the value of the attribute)
        qn1, qn2 = attr_pair_1[1], attr_pair_2[1]  # elements' id

        if qn1 and qn2:  # only proceed if both ends of the relation exist
            try:
                if qn1 not in node_map:
                    node_map[qn1] = INFERRED_ELEMENT_CLASS[attr_pair_1[0]](None, qn1)
                if qn2 not in node_map:
                    node_map[qn2] = INFERRED_ELEMENT_CLASS[attr_pair_2[0]](None, qn2)
            except KeyError:
                # Unsupported attribute; cannot infer the type of the element
                continue  # skipping this relation

            start_node = node_map[qn1]
            end_node = node_map[qn2]
            rel = prov_relation_to_edge(relation, start_node, end_node)

            graph = graph | rel
            
    return graph


def graph_to_prov(prov_document, nodes, edges):

    # then add element
    for node in nodes:
        if not node.has_label(NS_NODE_LABEL):
            node_to_prov_element(node, prov_document)

    # finally add relation
    for edge in edges:
        edge_to_prov_relation(edge, prov_document)

    return prov_document


# Read
@documents_bp.cli.command('get')
@click.option("--doc_id", default=None)
def get_document(doc_id):
    if doc_id is None:
        print(neo4j.get_all_dbs)
    else:
        # get db and check if it exists
        graph = neo4j.get_db(doc_id)
    
        try:
            assert graph
        except AssertionError:
            raise FileNotFoundError("Document not found")  # , 404
        else:
            node_matcher = NodeMatcher(graph)
            relationship_matcher = RelationshipMatcher(graph)
    
            nodes = node_matcher.match().all()
            ns_node = node_matcher.match(NS_NODE_LABEL).first()
            relationships = relationship_matcher.match().all()
    
            prov_document = ProvDocument()
            set_document_ns(ns_node, prov_document)
    
            prov_document = graph_to_prov(prov_document, nodes, relationships)
    
            print(prov_document)


# # Get list
# @documents_bp.cli.command('get-all')
# def get_list_of_documents():
#     print(eo4j.)  # get_all_dbs()


# Create
@documents_bp.cli.command('create')
@click.argument("doc_id")
@click.argument("file", type=click.Path(exists=True))
def upload_document(doc_id, file):
    # check if json
    if not os.path.isfile(file):
        raise FileNotFoundError("Please pass a valid path!")

    with open(file, 'r') as fp:
        if file.read(2) != '[]' and file.seek(0).read(2) != '{}':
            file.seek(0)
            data = json.load(fp)
        else:
            raise Exception("File must be not empty!")
    try:
        prov_document = ProvDocument.deserialize(content=data)
    except:
        raise SyntaxError("Document not valid!")
    
    # content_type = request.headers.get('Content-Type')
    # if content_type != 'application/json':
    #     print('Content-Type not supported!')  # , 400
    # 
    # try:
    #     # get the ProvDocument
    #     data = request.data
    #     prov_document = ProvDocument.deserialize(content=data)
    # except:
    #     print("Document not valid")  # , 400

    # parse ProvDocument to SubGraph  
    s = prov_to_graph(prov_document)

    graph = neo4j.get_db(doc_id)

    if not graph:
        # create db and set ns
        graph = neo4j.create_db(doc_id)
        graph.create(get_ns_node(prov_document))
    else:
        # update ns if necessary
        graph.push(get_ns_node(prov_document))

    # merge on anonymous label _Node and property id
    graph.merge(s, ELEMENT_NODE_PRIMARY_LABEL, ELEMENT_NODE_PRIMARY_ID)

    print("Document uploaded")  # , 201


# Delete
@documents_bp.cli.command('delete')
@click.argument("doc_id")
def delete_document(doc_id):
    db_list = []
    try:
        db_list = neo4j.get_all_dbs()
    except:
        raise SystemError("DB error")  # , 500
    
    if doc_id in db_list:
        try:
            neo4j.delete_db(doc_id)
        except:
            raise SystemError("DB error")  # , 500
        
        print("Document deleted")  # , 200
    else:
        raise FileNotFoundError("Document not found")  # , 404
        # print("Document not found")
        # exit()