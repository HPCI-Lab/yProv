import requests

PATH = "http://localhost:3000/api/v0/documents"

# path to use to create a docker image
#PATH = "http://web:3000/api/v0/documents"


TOKEN = None

def test_documents_put_doc_id():
    # document uploaded
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta', json=payload, headers=headers)
    assert response.status_code == 201

    """
    # document non valid
    payload = {"document non valid"}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id', json=payload, headers=headers)
    assert response.status_code == 400
    """


def test_documents_put_doc_id_permission():
    """
    # succesfully added access
    payload = {
        "[object Object]": "second_user",
        "level": "r"
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/permissions', json=payload, headers=headers)
    assert response.status_code == 201

    # data non valid
    payload = {
        "invalid data"
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/permissions', json=payload, headers=headers)
    assert response.status_code == 400

    # permission issue
    payload = {
        "[object Object]": "second_user",
        "level": "r"
    }
    headers = {
        'Authorization': 'Bearer wrong_token'
    }
    response = requests.put(PATH + '/pta/permissions', json=payload, headers=headers)
    assert response.status_code == 403

    # document not found
    payload = {
        "[object Object]": "second_user",
        "level": "r"
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id/permissions', json=payload, headers=headers)
    assert response.status_code == 404
    """

def test_documents_put_doc_id_entities_e_id():
    """
    # entity added
    payload = {}
    headers = {
       'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/entities/test', json=payload, headers=headers)
    assert response.status_code == 201

    # document not valid
    payload = { "document not valid" }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/entities/test', json=payload, headers=headers)
    assert response.status_code == 400

    # document not found
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id/entities/test', json=payload, headers=headers)
    assert response.status_code == 404
    """
    

def test_documents_put_doc_id_activities_a_id():
    """
    # activity added
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/activities/test', json=payload, headers=headers)
    assert response.status_code == 201

    # document not valid
    payload = { "document not valid" }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/activities/test', json=payload, headers=headers)
    assert response.status_code == 400

    # document not found
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id/activities/test', json=payload, headers=headers)
    assert response.status_code == 404
    """


def test_documents_put_doc_id_agents_a_id():
    """
    # agents added
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/agents/test', json=payload, headers=headers)
    assert response.status_code == 201

    # document not valid
    payload = { "document not valid" }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/agents/test', json=payload, headers=headers)
    assert response.status_code == 400

    # document not found
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id/agents/test', json=payload, headers=headers)
    assert response.status_code == 404
    """


def test_documents_put_doc_id_relations_r_id():
    """
    # agents added
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/relations/test', json=payload, headers=headers)
    assert response.status_code == 201

    # document not valid
    payload = { "document not valid" }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/relations/test', json=payload, headers=headers)
    assert response.status_code == 400

    # document not found
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id/relations/test', json=payload, headers=headers)
    assert response.status_code == 404
    """

def test_documents_get():
    # return the list of documents
    response = requests.get(PATH)
    assert response.status_code == 200


def test_documents_get_doc_id():
    # return the correct document
    response = requests.get(PATH + "/pta")
    assert response.status_code == 200

    # does not find the document
    response = requests.get(PATH + "/wrong_id")
    assert response.status_code == 404


def test_documents_get_doc_id_subgraph():
    # return requested subgraph
    QUERY = "?id=ophidia%3Ahttp%3A%2F%2F127.0.0.1%2Fophidia%2F66%2F7191"
    response = requests.get(PATH + "/pta/subgraph" + QUERY)
    assert response.status_code == 200

    # document not found
    QUERY = "?id=ophidia%3Ahttp%3A%2F%2F127.0.0.1%2Fophidia%2F66%2F7191"
    response = requests.get(PATH + "/wrong_id/subgraph" + QUERY)
    assert response.status_code == 404


def test_documents_get_doc_id_entities():
    # list of entities
    response = requests.get(PATH + "/pta/entities")
    assert response.status_code == 200

    # document not found
    response = requests.get(PATH + "/wrong_id/entities")
    assert response.status_code == 404


def test_documents_get_doc_id_activities():
    # list of activities
    response = requests.get(PATH + "/pta/activities")
    assert response.status_code == 200

    # document not found
    response = requests.get(PATH + "/wrong_id/activities")
    assert response.status_code == 404


def test_documents_get_doc_id_agents():
    # list of agents
    response = requests.get(PATH + "/pta/agents")
    assert response.status_code == 200

    # document not found
    response = requests.get(PATH + "/wrong_id/agents")
    assert response.status_code == 404


def test_documents_get_doc_id_entities_e_id():
    """
    # return requested entity
    response = requests.get(PATH + "/pta/entities/test")
    assert response.status_code == 200

    # document not found
    response = requests.get(PATH + "/wrong_id/entities/test")
    assert response.status_code == 404
    """


def test_documents_get_doc_id_activities_a_id():
    """
    # list of activities
    response = requests.get(PATH + "/pta/activities/test")
    assert response.status_code == 200

    # document not found
    response = requests.get(PATH + "/wrong_id/activities/test")
    assert response.status_code == 404
    """


def test_documents_get_doc_id_agents_a_id():
    """
    # list of agents
    response = requests.get(PATH + "/pta/agents/test")
    assert response.status_code == 200

    # document not found
    response = requests.get(PATH + "/wrong_id/agents/test")
    assert response.status_code == 404
    """


def test_documents_get_doc_id_relations_r_id():
    """
    # list of agents
    response = requests.get(PATH + "/pta/agents/test")
    assert response.status_code == 200

    # document not found
    response = requests.get(PATH + "/wrong_id/agents/test")
    assert response.status_code == 404
    """


def test_documents_delete_doc_id_entities_e_id():
    """
    # document uploaded
    headers = {
        'Authorization': 'Bearer wrong_token'
    }   
    response = requests.delete(PATH + '/pta/entities/test', headers=headers)
    assert response.status_code == 403
    
    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/entities/test', headers=headers)
    assert response.status_code == 200

    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/entities/test', headers=headers)
    assert response.status_code == 404
    """


def test_documents_delete_doc_id_activities_a_id():
    """
    # document uploaded
    headers = {
        'Authorization': 'Bearer wrong_token'
    }   
    response = requests.delete(PATH + '/pta/activites/test', headers=headers)
    assert response.status_code == 403
    
    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/activites/test', headers=headers)
    assert response.status_code == 200

    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/activites/test', headers=headers)
    assert response.status_code == 404
    """


def test_documents_delete_doc_id_agents_a_id():
    """
    # document uploaded
    headers = {
        'Authorization': 'Bearer wrong_token'
    }   
    response = requests.delete(PATH + '/pta/agents/test', headers=headers)
    assert response.status_code == 403
    
    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/agents/test', headers=headers)
    assert response.status_code == 200

    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/agents/test', headers=headers)
    assert response.status_code == 404
    """


def test_documents_delete_doc_id_relations_r_id():
    """
    # document uploaded
    headers = {
        'Authorization': 'Bearer wrong_token'
    }   
    response = requests.delete(PATH + '/pta/relations/test', headers=headers)
    assert response.status_code == 403
    
    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/relations/test', headers=headers)
    assert response.status_code == 200

    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/relations/test', headers=headers)
    assert response.status_code == 404
    """


def test_documents_delete_doc_id():
    """
    # document uploaded
    headers = {
        'Authorization': 'Bearer wrong_token'
    }   
    response = requests.delete(PATH + '/pta', headers=headers)
    assert response.status_code == 403
    """

    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta', headers=headers)
    assert response.status_code == 200

    # document uploaded
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta', headers=headers)
    assert response.status_code == 404

  

    


  