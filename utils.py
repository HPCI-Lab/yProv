from py2neo import Node
from prov2neo.encode import encode_value, str_id, node_label
from prov.constants import *
from prov.serializers.provjson import *


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

# based on decode_json_container at <https://github.com/trungdong/prov/blob/master/src/prov/serializers/provjson.py>
def json_element_to_prov_element(json, bundle):

    for rec_type_str, rec_content in json.items():
        # get the type of the record 
        rec_type = PROV_RECORD_IDS_MAP[rec_type_str]
        
        for rec_id, content in rec_content.items():
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