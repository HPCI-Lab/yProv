from prov.constants import *


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
    "wasGeneratedBy": [PROV_ATTR_ENTITY,  PROV_ATTR_ACTIVITY],
    "used": [PROV_ATTR_ACTIVITY, PROV_ATTR_ENTITY],
    "wasInformedBy": [PROV_ATTR_INFORMED, PROV_ATTR_INFORMANT],
    "wasStartedBy": [PROV_ATTR_ACTIVITY, PROV_ATTR_TRIGGER],
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

# graph merge
ELEMENT_NODE_PRIMARY_LABEL = '_ProvElementNode'
ELEMENT_NODE_PRIMARY_ID = 'id'
NS_NODE_LABEL = '_Namespace'
