from py2neo import Node

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
