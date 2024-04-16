from flask import request, Blueprint, jsonify
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
    set_document_ns,
    auth_required
)

from .utils.user_handling import *

documents_bp = Blueprint('documents', __name__)


def prov_to_graph(prov_document):
    graph = Subgraph()
    # Returns a new document containing all records having same identifiers unified (including those inside bundles)
    unified = prov_document.unified()
    node_map = dict()

    for element in unified.get_records(ProvElement):
        node = prov_element_to_node(element)
        graph = graph | node  # union operator: add Node to the Subgraph
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
@documents_bp.route('/<string:doc_id>', methods=['GET'])
@auth_required
def get_document(doc_id):
    token = request.headers["Authorization"].split(" ")[1]
    user = get_user(token)
    if not has_user_permission(user, doc_id, 'r', docs=True):
        return jsonify({'error': "User does not have permission to execute this operation on this document!"}), 403

    # get db and check if it exists
    graph = neo4j.get_db(doc_id)

    try:
        assert graph
    except AssertionError:
        return jsonify({'error': "Document not found"}), 404
    else:
        node_matcher = NodeMatcher(graph)
        relationship_matcher = RelationshipMatcher(graph)

        nodes = node_matcher.match().all()
        ns_node = node_matcher.match(NS_NODE_LABEL).first()
        relationships = relationship_matcher.match().all()

        prov_document = ProvDocument()
        set_document_ns(ns_node, prov_document)

        prov_document = graph_to_prov(prov_document, nodes, relationships)

        return jsonify({'result': prov_document.serialize()}), 200

# Get subgraph
@documents_bp.route('/<string:doc_id>/subgraph', methods=['GET'])
@auth_required                                                
def get_subgraph(doc_id):  

    token = request.headers["Authorization"].split(" ")[1]
    user = get_user(token)
    
    if not has_user_permission(user, doc_id, 'r', docs=True):
        return jsonify({'error': "User does not have permission to execute this operation on this document!"}), 403
    
    e_id = request.args.get('id')
    if not e_id:
        return jsonify({'error': "id is missing"}), 404                                                                                                           
    try:                                                                                                            
        graph = neo4j.get_db(doc_id)                                                                                
    except:                                                                                                         
        return jsonify({'error': "DB error"}), 500                                                                  
                                                                                                                    
    try:                                                                                                            
        assert graph                                                                                                
    except AssertionError:                                                                                          
        return jsonify({'error': "Document not found"}), 404                                                        
                                                                                                                    
    try:                                                                                                            
        query = """MATCH (n {id: $e_id}) CALL apoc.path.subgraphAll(n, {relationshipFilter:'>'}) YIELD nodes, relationships RETURN nodes, relationships"""
        subgraph = graph.run(query,parameters={'e_id':e_id}).data()                                                                           
    except:                                                                                                                                   
        return jsonify({'error': "DB error"}), 500    
                                                               
    try:                                                                                                                                       
        nodes = subgraph[0]['nodes']                                                                                
        relationships = subgraph[0]['relationships'] 
        
        node_matcher = NodeMatcher(graph)                                                                           
        relationship_matcher = RelationshipMatcher(graph)                                                                                     
        ns_node = node_matcher.match(NS_NODE_LABEL).first()                                                                                        
        prov_document = ProvDocument()                                                                                                         
        set_document_ns(ns_node, prov_document)                                                                                            
        prov_document = graph_to_prov(prov_document, nodes, relationships)                                                                     
        
        return jsonify({'result': prov_document.serialize()}), 200
    except:
        return jsonify({'error': "Subgraph not found"}), 404
    
# Get list
@documents_bp.route('', methods=['GET'])
def get_list_of_documents():
    return jsonify({'result': neo4j.get_all_dbs()}), 200


# Create
@documents_bp.route('/<string:doc_id>', methods=['PUT'])
@auth_required
def upload_document(doc_id):
    # check if json
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({'error': 'Content-Type not supported!'}), 400

    try:
        # get the ProvDocument
        data = request.data
        prov_document = ProvDocument.deserialize(content=data)

    except:
        return jsonify({'error': "Document not valid"}), 400

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

    # add user permission to modify graph
    token = request.headers["Authorization"].split(" ")[1]
    user = get_user(token)
    add_new_graph(user, doc_id)

    # merge on anonymous label _Node and property id
    graph.merge(s, ELEMENT_NODE_PRIMARY_LABEL, ELEMENT_NODE_PRIMARY_ID)

    return jsonify({'message': "Document uploaded"}), 201


# Delete
@documents_bp.route('/<string:doc_id>', methods=['DELETE'])
@auth_required
def delete_document(doc_id):
    db_list = []

    token = request.headers["Authorization"].split(" ")[1]
    user = get_user(token)
    if not has_user_permission(user, doc_id, 'd', docs=True):
        return jsonify({'error': "User does not have permission to execute this operation on this document!"}), 403

    try:
        db_list = neo4j.get_all_dbs()
    except:
        return jsonify({'error': "DB error"}), 500

    if doc_id in db_list:
        try:
            neo4j.delete_db(doc_id)
        except:
            return jsonify({'error': "DB error"}), 500

        return jsonify({'message': "Document deleted"}), 200
    else:
        return jsonify({'error': "Document not found"}), 404


@documents_bp.route('/<string:doc_id>/permissions', methods=['PUT'])
@auth_required
def add_user_access_to_graph(doc_id):
    # check if json
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return jsonify({'error': 'Content-Type not supported!'}), 400

    token = request.headers["Authorization"].split(" ")[1]
    user = get_user(token)
    if not has_user_permission(user, doc_id, 'n', docs=True):
        return jsonify({'error': "User does not have permission to execute this operation on this document!"}), 403

    try:
        data = request.json
        if not ("user" in data and "level" in data) or \
            (data["user"] is None or data["user"] == "") or \
            (data["level"] is None or data["level"] == ""):
                raise Exception
    except:
        return jsonify({'error': "Data not valid"}), 400

    if user == data["user"]:
        return jsonify({'error': "Cannot modify owner permission. Graph must have a owner!"}), 403
    
    if not is_graph_valid(doc_id):
        return jsonify({'error': "Database not present!"}), 404

    if not check_user_presence(data["user"]):
        return jsonify({'error': "User not present in the system. Registration is needed!"}), 403

    if not data["level"] in ['o', 'r', 'w']:
        return jsonify({'error': "Level requested does not exists!"}), 403

    if data["level"] == 'o':
        return jsonify({'error': "Only one owner is possible for each db!"}), 403

    add_new_user_permission(data["user"], doc_id, data["level"])

    return jsonify({'message': "Successfully added access to the db!"}), 201
