from flask import Blueprint, request, jsonify

from prov.model import ProvDocument
from py2neo.matching import NodeMatcher

from extensions import neo4j

from .utils import (
    NS_NODE_LABEL,
    json_to_prov_record,
    prov_element_to_node,
    node_to_prov_element,
    prov_element_to_json,
    set_document_ns,
    auth_required
)

from .utils.user_handling import *

entities_bp = Blueprint('entities', __name__)


# Create
@entities_bp.route('', methods=['POST'])
@auth_required
def create_entity(doc_id):
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
        assert graph
    except AssertionError:
        return jsonify({'error': "Document not found"}), 404

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    # parsing
    prov_element = json_to_prov_record(request.json, prov_document)
    node = prov_element_to_node(prov_element)

    try:
        graph.create(node)
    except:
        return jsonify({'error': "DB error"}), 500

    return jsonify({'message': "Entity created"}), 201


# Read
@entities_bp.route('/<string:e_id>', methods=['GET'])
@auth_required
def get_entity(doc_id, e_id):
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

    # check if element is in document
    try:
        # match the node
        node_matcher = NodeMatcher(graph)
        node = node_matcher.match('Entity', id=e_id).first()
        assert node
    except AssertionError:
        return jsonify({'error': "Entity not found"}), 404

    # create ProvDocument and add namespaces
    prov_document = ProvDocument()
    node_matcher = NodeMatcher(graph)
    ns_node = node_matcher.match(NS_NODE_LABEL).first()
    set_document_ns(ns_node, prov_document)

    prov_element = node_to_prov_element(node, prov_document)

    return jsonify(prov_element_to_json(prov_element)), 200


# Update
@entities_bp.route('/<string:e_id>', methods=['PUT'])
@auth_required
def replace_entity(doc_id, e_id):
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
        assert graph
    except AssertionError:
        return jsonify({'error': "Document not found"}), 404

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
    prov_element = json_to_prov_record(request.json, prov_document)
    input_node = prov_element_to_node(prov_element)

    # if exist then update else create
    if node:
        node.clear()
        for key, value in input_node.items():
            node[key] = value

        graph.push(node)

        return jsonify({'message': "Entity updated"}), 200
    else:
        try:
            graph.create(input_node)
        except:
            return jsonify({'error': "DB error"}), 500

        return jsonify({'message': "Entity created"}), 201


# Delete
@entities_bp.route('/<string:e_id>', methods=['DELETE'])
@auth_required
def delete_entity(doc_id, e_id):
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

    # check if element is in document
    try:
        # match the node
        node_matcher = NodeMatcher(graph)
        node = node_matcher.match('Entity', id=e_id).first()
        # node = node_matcher.match(id=e_id).first()
        assert node
    except AssertionError:
        return jsonify({'error': "Element not found"}), 404

    try:
        graph.delete(node)
    except AssertionError:
        return jsonify({'error': "DB error"}), 500

    return jsonify({'message': "Element deleted"}), 200
