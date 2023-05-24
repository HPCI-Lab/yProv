from py2neo.data import Node, Relationship
from prov2neo.encode import encode_value, str_id, node_label, edge_label

from .constants import ELEMENT_NODE_PRIMARY_LABEL

import uuid

def prov_element_to_node(prov_element):
    # parse attr to props
    props = dict()
    for attr in prov_element.attributes:
        props[encode_value(attr[0])] = encode_value(attr[1])
    labels = [node_label(prov_element), ELEMENT_NODE_PRIMARY_LABEL]
    return Node(
        *labels,
        id = str_id(prov_element.identifier),
        **props
    )

def prov_relation_to_edge(prov_relation, start_node, end_node):
    # parse attr to props
    props = {}

    # skip first two attrs (e.g. the two nodes)
    for attr in prov_relation.formal_attributes[2:]:
        props[encode_value(attr[0])] = encode_value(attr[1])

    # extra attr
    for attr in prov_relation.extra_attributes:
        props[encode_value(attr[0])] = encode_value(attr[1])
    
    if not prov_relation.identifier:
        props['id'] = str(uuid.uuid4())
    else:
        props['id'] = str(prov_relation.identifier)
        
    return Relationship(
        start_node,
        edge_label(prov_relation),
        end_node,
        **props
    )
