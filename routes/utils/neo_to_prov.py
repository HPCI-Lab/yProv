from prov.constants import *
from prov.serializers.provjson import *

from .constants import ELEMENT_NODE_PRIMARY_LABEL, ELEMENT_NODE_PRIMARY_ID, MAP_PROV_REL_TYPES


def type_of_prov_node(node):
    for label in node.labels:
        if not label == ELEMENT_NODE_PRIMARY_LABEL:
            return PROV_RECORD_IDS_MAP[label.lower()]


def encode_literal(value):
    separator = '%%'
    if separator in value:

        literal = value.split(separator)
        v = literal[0].replace('\"', '')
        dt = literal[1]

        return Literal(v, dt)
    else:
        # simple type, just return it
        return value


def node_to_prov_element(node, bundle):

    rec_type = type_of_prov_node(node)
    
    attributes = []
    other_attributes = []

    #  bit from decode_json_container at
    #  <https://github.com/trungdong/prov/blob/master/src/prov/serializers/provjson.py>
    for attr_name, value in node.items():
        attributes = dict()
        if not attr_name == ELEMENT_NODE_PRIMARY_ID:
            attr = (
                PROV_ATTRIBUTES_ID_MAP[attr_name]
                if attr_name in PROV_ATTRIBUTES_ID_MAP
                else valid_qualified_name(bundle, attr_name)
            )
            if attr in PROV_ATTRIBUTES:
                value = (
                    valid_qualified_name(bundle, value)
                    if attr in PROV_ATTRIBUTE_QNAMES
                    # else parse_xsd_datetime(value)
                    # TypeError: Parser must be a string or character stream, not DateTime
                    else str(value)
                )
                attributes[attr] = value
            else:
                other_attributes.append(
                    (attr, encode_literal(value))
                )
        else:
            rec_id = value

    return bundle.new_record(rec_type, rec_id, attributes, other_attributes)


def edge_to_prov_relation(edge, bundle):

    rec_type_str = type(edge).__name__
    rec_type = PROV_RECORD_IDS_MAP[rec_type_str]  # e.g wasDerivedFrom': <QualifiedName: prov:Derivation>

    # easy unique id
    rec_id = '_id:' + str(edge.identity)
    
    attributes = dict()
    other_attributes = []

    # array with prov qnames of nodes of the relaion
    node_pair_qnames = MAP_PROV_REL_TYPES[rec_type_str]

    # append first two attributes (always present)
    for node in {edge.start_node, edge.end_node}:
        if node == edge.start_node:
            qname = node_pair_qnames[0]
        else:
            qname = node_pair_qnames[1]

        id = node['id']
        attributes[qname] = id


    # again this bit from decode_json_container at
    # <https://github.com/trungdong/prov/blob/master/src/prov/serializers/provjson.py>

    for attr_name, value in edge.items():
        if not attr_name == 'id':
            attr = (
                PROV_ATTRIBUTES_ID_MAP[attr_name]
                if attr_name in PROV_ATTRIBUTES_ID_MAP
                else valid_qualified_name(bundle, attr_name)
            )
            if attr in PROV_ATTRIBUTES:
                value = (
                    valid_qualified_name(bundle, value)
                    if attr in PROV_ATTRIBUTE_QNAMES
                    # else parse_xsd_datetime(value)
                    # TypeError: Parser must be a string or character stream, not DateTime
                    else str(value)
                )
                attributes[attr] = value
            else:
                '''
                    sistemare prov role finisce qua
                '''
                other_attributes.append(
                    (attr, encode_literal(value))
                )
        else:
            rec_id = value
    
    return bundle.new_record(rec_type, rec_id, attributes, other_attributes)
