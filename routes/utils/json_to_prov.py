from prov.constants import *
from prov.serializers.provjson import *


# based on decode_json_container at <https://github.com/trungdong/prov/blob/master/src/prov/serializers/provjson.py>
def json_to_prov_record(json_file, bundle):

    for rec_type_str, rec_content in json_file.items():
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
