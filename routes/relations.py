from flask import Blueprint, request, jsonify

from prov.model import ProvDocument
from py2neo.matching import RelationshipMatcher, NodeMatcher

from extensions import neo4j
from .utils import (
    NS_NODE_LABEL,
    json_to_prov_record,
    prov_relation_to_edge,
    edge_to_prov_relation,
    prov_relation_to_json,
    set_document_ns,
    auth_required
)

from .utils.user_handling import *

relations_bp = Blueprint('relations', __name__)


# Create
@relations_bp.route('', methods=['POST'])
@auth_required
def create_relation(doc_id):
    token = request.args.get('token')
    user = get_user(token)
    if not has_user_permission(user, doc_id, 'c'):
        return jsonify({'error': "User does not have permission to execute this operation on this document!"}), 403

    try:
        graph = neo4j.get_db(doc_id)
    except:
        return jsonify({'error': "DB error"}), 500

    # check if document is in neo4j
    try:
        assert graph, "Document not found"
    except AssertionError as aerr:
        return jsonify({'error': str(aerr)}), 404

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    # parsing
    prov_relation = json_to_prov_record(request.json, prov_document)

    # taking the first two elements of a relation
    attr_pair_1, attr_pair_2 = prov_relation.formal_attributes[:2]
    id1, id2 = str(attr_pair_1[1]), str(attr_pair_2[1])  # sono gli id degli elementi

    if id1 and id2:  # only proceed if both ends of the relation exist
        node_matcher = NodeMatcher(graph)

        start_node = node_matcher.match(id=id1).first()
        end_node = node_matcher.match(id=id2).first()

        try:
            assert start_node, "Start node not found"
            assert end_node, "End node not found"
        except AssertionError as aerr:
            return jsonify({'error': str(aerr)}), 400

        rel = prov_relation_to_edge(prov_relation, start_node, end_node)

        try:
            graph.create(rel)
        except:
            return jsonify({'error': "DB error"}), 500

        return jsonify({'message': "Relation created"}), 201


# Read
@relations_bp.route('/<string:r_id>', methods=['GET'])
@auth_required
def get_relation(doc_id, r_id):
    token = request.args.get('token')
    user = get_user(token)
    if not has_user_permission(user, doc_id, 'r'):
        return jsonify({'error': "User does not have permission to execute this operation on this document!"}), 403

    try:
        graph = neo4j.get_db(doc_id)
    except:
        return jsonify({'error': "DB error"}), 500

    # check if document is in neo4j
    try:
        assert graph
    except AssertionError:
        return jsonify({'error': "Document not found"}), 404

    # check if relation is in document
    # match the rel
    rel_matcher = RelationshipMatcher(graph)
    rel = rel_matcher.match(id=r_id).first()
    try:
        assert rel
    except AssertionError:
        return jsonify({'error': "Relation not found"}), 404

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    prov_relation = edge_to_prov_relation(rel, prov_document)

    return jsonify(prov_relation_to_json(prov_relation)), 200


# Update
@relations_bp.route('/<string:r_id>', methods=['PUT'])
@auth_required
def replace_relation(doc_id, r_id):
    token = request.args.get('token')
    user = get_user(token)
    if not has_user_permission(user, doc_id, 'u'):
        return jsonify({'error': "User does not have permission to execute this operation on this document!"}), 403

    try:
        graph = neo4j.get_db(doc_id)
    except:
        return jsonify({'error': "DB error"}), 500

    # check if document is in neo4j
    try:
        assert graph, "Document not found"
    except AssertionError as aerr:
        return jsonify({'error': str(aerr)}), 404

    # check if relation is in document
    # match the rel
    rel_matcher = RelationshipMatcher(graph)
    old_rel = rel_matcher.match(id=r_id).first()

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    # parsing
    input_prov_relation = json_to_prov_record(request.json, prov_document)

    if str(input_prov_relation.identifier) != r_id:
        # incongruenza
        return jsonify({'error': "Relation id in URI and JSON differ"}), 400

    # taking the first two elements of a relation
    attr_pair_1, attr_pair_2 = input_prov_relation.formal_attributes[:2]
    id1, id2 = str(attr_pair_1[1]), str(attr_pair_2[1])  # sono gli id degli elementi

    if id1 and id2:  # only proceed if both ends of the relation exist
        node_matcher = NodeMatcher(graph)

        start_node = node_matcher.match(id=id1).first()
        end_node = node_matcher.match(id=id2).first()

        try:
            assert start_node, "Start node not found"
            assert end_node, "End node not found"
        except AssertionError as aerr:
            return jsonify({'error': str(aerr)}), 400

    new_rel = prov_relation_to_edge(input_prov_relation, start_node, end_node)

    if old_rel:
        try:
            # update
            old_rel.clear()
            for key, value in new_rel.items():
                if not key == 'id':
                    old_rel[key] = value
            old_rel['id'] = r_id
            graph.push(old_rel)
        except:
            return jsonify({'error': "DB error"}), 500

        return jsonify({'message': "Relation updated"}), 200
    else:
        try:
            graph.create(new_rel)
        except:
            return jsonify({'error': "DB error"}), 500

        return jsonify({'message': "Relation created"}), 201


# Delete
@relations_bp.route('/<string:r_id>', methods=['DELETE'])
@auth_required
def delete_relation(doc_id, r_id):
    token = request.args.get('token')
    user = get_user(token)
    if not has_user_permission(user, doc_id, 'd'):
        return jsonify({'error': "User does not have permission to execute this operation on this document!"}), 403

    try:
        graph = neo4j.get_db(doc_id)
    except:
        return jsonify({'error': "DB error"}), 500

    # check if document is in neo4j
    try:
        assert graph
    except AssertionError:
        return jsonify({'error': "Document not found"}), 404

    # check if relation is in document
    try:
        # match the rel
        rel_matcher = RelationshipMatcher(graph)
        rel = rel_matcher.match(id=r_id).first()
        assert rel
    except AssertionError:
        return jsonify({'error': "Relation not found"}), 404

    try:
        graph.separate(rel)
    except AssertionError:
        return jsonify({'error': "DB error"}), 500

    return jsonify({'message': "Relation deleted"}), 200
