from py2neo.data import Node, Relationship
from prov2neo.encode import encode_value, str_id, node_label, edge_label
from prov.model import first, ProvRelation
from prov.constants import *
from prov.serializers.provjson import *

import uuid


# map wich assign foreach PROV-DM Relation its binary(subject, object) PROV-DM Types
# Note: every core relation in PROV-DM is binary
'''
mapProvRelTypes= {
    "wasGeneratedBy": ["prov:entity", "prov:activity"],
    "used": ["prov:activity", "prov:entity"],
    "wasInformedBy": ["prov:informed", "prov:informant"],
    "wasStartedBy":["prov:activity", "prov:trigger"],
    "wasEndedBy": ["prov:activity", "prov:trigger"],
    "wasInvalidatedBy": ["prov:entity", "prov:activity"],
    "wasDerivedFrom": ["prov:generatedEntity", "prov:usedEntity"],
    "wasAttributedTo": ["prov:entity", "prov:agent"],
    "wasAssociatedWith": ["prov:activity", "prov:agent"],
    "actedOnBehalfOf": ["prov:delegate", "prov:responsible"],
    "wasInfluencedBy": ["prov:influencee", "prov:influencer"],
    "specializationOf": ["prov:specificEntity", "prov:generalEntity"],
    "alternateOf": ["prov:alternate1", "prov:alternate2"],
    "hadMember": ["prov:collection", "prov:entity"]             
}
'''
MAP_PROV_REL_TYPES = {
    "wasGeneratedBy": [ PROV_ATTR_ENTITY,  PROV_ATTR_ACTIVITY],
    "used": [PROV_ATTR_ACTIVITY, PROV_ATTR_ENTITY],
    "wasInformedBy": [PROV_ATTR_INFORMED, PROV_ATTR_INFORMANT],
    "wasStartedBy":[PROV_ATTR_ACTIVITY, PROV_ATTR_TRIGGER],
    "wasEndedBy": [PROV_ATTR_ACTIVITY, PROV_ATTR_TRIGGER],
    "wasInvalidatedBy": [PROV_ATTR_ENTITY, PROV_ATTR_ACTIVITY],
    "wasDerivedFrom": [PROV_ATTR_GENERATED_ENTITY, PROV_ATTR_USED_ENTITY],
    "wasAttributedTo": [PROV_ATTR_ENTITY, PROV_ATTR_AGENT],
    "wasAssociatedWith": [PROV_ATTR_ACTIVITY, PROV_ATTR_AGENT],
    "actedOnBehalfOf": [PROV_ATTR_DELEGATE, PROV_ATTR_RESPONSIBLE],
    "wasInfluencedBy": [PROV_ATTR_INFLUENCEE, PROV_ATTR_INFLUENCER],
    "specializationOf": [PROV_ATTR_SPECIFIC_ENTITY, PROV_ATTR_GENERAL_ENTITY],
    "alternateOf": [PROV_ATTR_ALTERNATE1, PROV_ATTR_ALTERNATE2],
    "hadMember": [PROV_ATTR_COLLECTION, PROV_ATTR_ENTITY]             
}


def json_to_node(json):
    # get label, id and props of the element
    node_label = list(json.keys())[0]
    node_id = list(json[node_label].keys())[0]
    node_props = json[node_label][node_id]

    # create and return node instance    
    return Node(node_label.capitalize(), id=node_id, **node_props)

def node_to_json(node, type):
    # construct the return JSON
    element_id = ''
    element_props = {}
    for key in node.keys():
        if(key=='id'):
            element_id = node[key]
        else:
            element_props[key] = node[key]

    return {
        type : {
            element_id : element_props
        }
    }


def set_ns(graph, bundle):
    default = False
    # get the ns of the document            
    for ns in graph.call.n10s.nsprefixes.list():
        if(ns[0]=='default'):
            bundle.set_default_namespace(ns[1])
            default=True
        else:
            bundle.add_namespace(ns[0], ns[1])
    if not default:
        bundle.set_default_namespace('')


'''
    json_to_prov.js
'''
# based on decode_json_container at <https://github.com/trungdong/prov/blob/master/src/prov/serializers/provjson.py>
def json_to_prov_record(json, bundle):

    for rec_type_str, rec_content in json.items():
        # get the type of the record 
        rec_type = PROV_RECORD_IDS_MAP[rec_type_str]
        
        for rec_id, content in rec_content.items():
            print(rec_id)
            if hasattr(content, "items"):  # it is a dict
                #  There is only one element, create a singleton list
                elements = [content]
            else:
                # expect it to be a list of dictionaries
                elements = content

            for element in elements:
                attributes = dict()
                other_attributes = []
                # this is for the multiple-entity membership hack to come
                membership_extra_members = None
                for attr_name, values in element.items():
                    attr = (
                        PROV_ATTRIBUTES_ID_MAP[attr_name]
                        if attr_name in PROV_ATTRIBUTES_ID_MAP
                        else valid_qualified_name(bundle, attr_name)
                    )
                    if attr in PROV_ATTRIBUTES:
                        if isinstance(values, list):
                            # only one value is allowed
                            if len(values) > 1:
                                # unless it is the membership hack
                                if (
                                    rec_type == PROV_MEMBERSHIP
                                    and attr == PROV_ATTR_ENTITY
                                ):
                                    # This is a membership relation with
                                    # multiple entities
                                    # HACK: create multiple membership
                                    # relations, one for each entity

                                    # Store all the extra entities
                                    membership_extra_members = values[1:]
                                    # Create the first membership relation as
                                    # normal for the first entity
                                    value = values[0]
                                else:
                                    error_msg = (
                                        "The prov package does not support PROV"
                                        " attributes having multiple values."
                                    )
                                    logger.error(error_msg)
                                    raise ProvJSONException(error_msg)
                            else:
                                value = values[0]
                        else:
                            value = values
                        value = (
                            valid_qualified_name(bundle, value)
                            if attr in PROV_ATTRIBUTE_QNAMES
                            else parse_xsd_datetime(value)
                        )
                        attributes[attr] = value
                    else:
                        if isinstance(values, list):
                            other_attributes.extend(
                                (attr, decode_json_representation(value, bundle))
                                for value in values
                            )
                        else:
                            # single value
                            other_attributes.append(
                                (attr, decode_json_representation(values, bundle))
                            )
                        
        bundle.new_record(rec_type, rec_id, attributes, other_attributes)

    #prov_element = bundle.get_record(rec_id)[0]
    # prov_element = prov_document.get_records(ProvElement)[0]
    return bundle.get_record(rec_id)[0]


'''
    neo_to_prov.js
'''
def type_of_prov_node(node):
    type_str = list(node.labels)[0].lower()
    return PROV_RECORD_IDS_MAP[type_str]

def encode_literal(value):
    separator = '%%'
    if (separator in value):

        literal = value.split(separator)
        v=literal[0].replace('\"','')
        dt=literal[1]

        return Literal(v, dt)
    else:
        # simple type, just return it
        return value

def node_to_prov_element(node, bundle):

    rec_type = type_of_prov_node(node)
    
    attributes = []
    other_attributes = []

    #  bit from decode_json_container at <https://github.com/trungdong/prov/blob/master/src/prov/serializers/provjson.py>
    for attr_name, value in node.items():
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
                    # else parse_xsd_datetime(value) # TypeError: Parser must be a string or character stream, not DateTime
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
    rec_type = PROV_RECORD_IDS_MAP[rec_type_str]    #e.g wasDerivedFrom': <QualifiedName: prov:Derivation>

    attributes = dict()
    other_attributes = []

    # array with prov qnames of nodes of the relaion
    node_pair_qnames= MAP_PROV_REL_TYPES[rec_type_str]

    # append first two attributes (always present)
    for node in {edge.start_node, edge.end_node}:
        if(node == edge.start_node):
            qname = node_pair_qnames[0]
        else:
            qname = node_pair_qnames[1]

        id = node['id']
        attributes[qname] =  id


    # again this bit from decode_json_container at <https://github.com/trungdong/prov/blob/master/src/prov/serializers/provjson.py>

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
                    # else parse_xsd_datetime(value) # TypeError: Parser must be a string or character stream, not DateTime
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


'''
    prov_to_json.js
'''
# from encode_json_container at <https://github.com/trungdong/prov/blob/master/src/prov/serializers/provjson.py>
def encode_attributes(record):
    record_json = {}
    if record._attributes:
        for (attr, values) in record._attributes.items():
            if not values:
                continue
            attr_name = str(attr)
            if attr in PROV_ATTRIBUTE_QNAMES:
                # TODO: QName export
                record_json[attr_name] = str(first(values))
            elif attr in PROV_ATTRIBUTE_LITERALS:
                record_json[attr_name] = first(values).isoformat()
            else:
                if len(values) == 1:
                    # single value
                    record_json[attr_name] = encode_json_representation(
                        first(values)
                    )
                else:
                    # multiple values
                    record_json[attr_name] = list(
                        encode_json_representation(value) for value in values
                    )
    return record_json

def prov_element_to_json(prov_element):

    rec_label = PROV_N_MAP[prov_element.get_type()]
    identifier = str(prov_element._identifier)
    attributes = encode_attributes(prov_element)

    return {
        rec_label : {
            identifier : attributes
        }
    }

def prov_relation_to_json(prov_element):

    rec_label = PROV_N_MAP[prov_element.get_type()]
    identifier = str(prov_element._identifier)
    attributes = encode_attributes(prov_element)

    return {
        rec_label : {
            identifier : attributes
        }
    }


'''
    prov_to_neo.js
'''
def prov_element_to_node(prov_element):
    # parse attr to props
    props = {}
    for attr in prov_element.attributes:
        props[encode_value(attr[0])] = encode_value(attr[1])
        
    return Node(
        node_label(prov_element),
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
