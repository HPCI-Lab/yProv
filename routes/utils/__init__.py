from .json_to_prov import json_to_prov_record
from .prov_to_json import prov_element_to_json, prov_relation_to_json

from .neo_to_prov import node_to_prov_element, edge_to_prov_relation
from .prov_to_neo import prov_element_to_node, prov_relation_to_edge

from .constants import *

from py2neo import Node

# handling neo4j ns
def get_ns_node(prov_document):
    ns_node = Node(NS_NODE_LABEL)
    default_ns = prov_document.get_default_namespace()
    if(default_ns):
        ns_node['default'] = default_ns._uri
    for ns in prov_document.get_registered_namespaces():
        ns_node[ns._prefix] = ns._uri
    return ns_node

def set_document_ns(ns_node, bundle):
    default = False
    for attr_name, value in ns_node.items():
        if attr_name =='default':
            bundle.set_default_namespace(value)
            default=True
        else:
            bundle.add_namespace(attr_name, value)
    if not default:
        # for relationships
        bundle.set_default_namespace('')
