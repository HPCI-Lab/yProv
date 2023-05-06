from flask import Blueprint, request

from prov.model import ProvDocument
from py2neo.matching import NodeMatcher, RelationshipMatcher

from extension import neo4j
from utils import json_element_to_prov_element, prov_element_to_node, node_to_prov_element, prov_element_to_json


relations_bp = Blueprint('relations', __name__)



# Create a relation
@relations_bp.route('', methods=['POST'])
def create_relations(doc_id):

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

    return "New relation created", 201