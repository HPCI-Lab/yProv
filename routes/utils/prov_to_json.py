from prov.model import first
from prov.serializers.provjson import *

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
