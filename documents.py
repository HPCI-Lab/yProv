from flask import Blueprint, jsonify, request
from prov.model import ProvDocument, ProvElement, ProvRelation
from prov.serializers.provjson import ProvJSONDecoder
from py2neo.data import Subgraph, Node, Relationship
from prov2neo.encode import encode_graph

from extension import neo4j

documents_bp = Blueprint('documents', __name__)

def elem_to_node(element):
    print(element.identifier.__str__())
    return Node(
        id = str(element.identifier)
    )


def prov_to_graph(prov_document):

    s = Subgraph()
    # Returns a new document containing all records having same identifiers unified (including those inside bundles)
    unified = prov_document.unified()
    node_map = dict()

    for element in unified.get_records(ProvElement):
        # union operator: add Node to the Subgraph
        s = s | elem_to_node(element)
        node_map[element.identifier] = element

    '''
    for relation in unified.get_records(ProvRelation):
        # taking the first two elements of a relation
        attr_pair_1, attr_pair_2 = relation.formal_attributes[:2]
        # only need the QualifiedName (i.e. the value of the attribute)
        qn1, qn2 = attr_pair_1[1], attr_pair_2[1]
        if qn1 and qn2:  # only proceed if both ends of the relation exist
            try:
                if qn1 not in node_map:
                    node_map[qn1] = INFERRED_ELEMENT_CLASS[attr_pair_1[0]](None, qn1)
                if qn2 not in node_map:
                    node_map[qn2] = INFERRED_ELEMENT_CLASS[attr_pair_2[0]](None, qn2)
            except KeyError:
                # Unsupported attribute; cannot infer the type of the element
                continue  # skipping this relation
            g.add_edge(node_map[qn1], node_map[qn2], relation=relation)
    '''
    return s


# Get a document
@documents_bp.route('/<string:doc_id>', methods=['GET'])
def get_document(doc_id):

    # get db and check if exists
    graph_db = neo4j.get_db(doc_id)

    try:
        assert graph_db
    except AssertionError:
        # no document
        return "No document", 400
    else:        
        return "Here it is your document"

# Get list of documents
@documents_bp.route('', methods=['GET'])
def get_list_documents():
    return neo4j.get_all_dbs()

# Create a document
@documents_bp.route('/<string:doc_id>', methods=['PUT'])
def create_document(doc_id):
    # check if json
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return 'Content-Type not supported!'
    
    # get db and check if exists
    graph_db = neo4j.get_db(doc_id)
    try:
        assert not graph_db
    except AssertionError:
        return "Document already exists", 400   
    else:
        graph_db = neo4j.create_db(doc_id)
        data = request.data
        prov_document = ProvDocument.deserialize(content=data)

        # prov2neo function (works also with bundles)
        s = encode_graph(prov_document) 

        graph_db.create(s)
        
        return "Document created", 201
    
# Delete a document
@documents_bp.route('/<string:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    try:
        neo4j.delete_db(doc_id)
    except:
        return "Document doesnt exist", 404
    else:
        return "Document deleted", 201