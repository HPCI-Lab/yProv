from flask import request, Response, Blueprint
from prov.model import ProvDocument, ProvElement, ProvRelation
from prov.graph import INFERRED_ELEMENT_CLASS
from py2neo.data import Subgraph
from py2neo.matching import NodeMatcher, RelationshipMatcher
# from prov2neo.encode import encode_graph

from extension import neo4j
from utils import (
    prov_element_to_node, 
    prov_relation_to_edge,
    node_to_prov_element,
    edge_to_prov_relation,
    set_ns
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
        qn1, qn2 = attr_pair_1[1], attr_pair_2[1] # sono gli id degli elementi

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


def graph_to_prov(graph, nodes, edges):

    prov_document = ProvDocument()

    # add namespace
    set_ns(graph, prov_document)

    # then add element
    for n in nodes:
        if not n.has_label('_NsPrefDef'):
            node_to_prov_element(n, prov_document)

    # finally add relation
    for e in edges:
        edge_to_prov_relation(e, prov_document)

    return prov_document



# Read
@documents_bp.route('/<string:doc_id>', methods=['GET'])
def get_document(doc_id):
    # get db and check if it exists
    graph = neo4j.get_db(doc_id)

    try:
        assert graph
    except AssertionError:
        return "Document not found", 404
    else:
        node_matcher = NodeMatcher(graph)
        relationship_matcher = RelationshipMatcher(graph)

        node_match = node_matcher.match()
        nodes = node_match.all()
        relationships = relationship_matcher.match().all()

        prov_document = graph_to_prov(graph, nodes, relationships)

        return Response(prov_document.serialize(), mimetype='application/json')

# Get list
@documents_bp.route('', methods=['GET'])
def get_documents_list():
    return neo4j.get_all_dbs()

# Create
@documents_bp.route('/<string:doc_id>', methods=['PUT'])
def create_document(doc_id):
    # check if json
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!', 400
    
    try:
        # get the ProvDocument
        data = request.data
        prov_document = ProvDocument.deserialize(content=data)
    except:
        return "Document not valid", 400 

    # translate ProvDocument to SubGraph  
    s = prov_to_graph(prov_document)

    graph = neo4j.get_db(doc_id)
    if(graph):
        graph.delete_all()
    else:
        # create db and save doc
        graph = neo4j.create_db(doc_id)
    
    graph.create(s)
    # add ns
    default_ns = prov_document.get_default_namespace()
    if(default_ns):
        graph.call.n10s.nsprefixes.add('default', default_ns._uri)
    for ns in prov_document.get_registered_namespaces():
        graph.call.n10s.nsprefixes.add(ns._prefix, ns._uri)

    return "Document created", 201      

# Delete
@documents_bp.route('/<string:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    db_list = []
    try:
        db_list = neo4j.get_all_dbs()
    except:
        return "DB error", 500
    
    if(doc_id in db_list):
        try:
            neo4j.delete_db(doc_id)
        except:
            return "DB error", 500
        
        return "Document deleted", 200
    else:
        return "Document not found", 404