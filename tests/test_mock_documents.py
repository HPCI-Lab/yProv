"""
import pytest
import responses
import requests

# URL dell'API
PATH = "http://web:3000/api/v0/documents"
TOKEN = "test_token"

@responses.activate
def test_documents_put_doc_id():
    # Mock per document uploaded
    responses.add(
        responses.PUT,
        f"{PATH}/pta",
        json={"message": "Document uploaded successfully"},
        status=201
    )

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Document uploaded successfully"}

    # Mock per document non valid
    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {"document non valid"}
    response = requests.put(PATH + '/wrong_id', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}

@responses.activate
def test_documents_put_doc_id_permission():
    # Mock per successfully added access
    responses.add(
        responses.PUT,
        f"{PATH}/pta/permissions",
        json={"message": "Access added successfully"},
        status=201
    )

    payload = {
        "[object Object]": "second_user",
        "level": "r"
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/permissions', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Access added successfully"}

    # Mock per data non valid
    responses.add(
        responses.PUT,
        f"{PATH}/pta/permissions",
        json={"error": "Invalid data"},
        status=400
    )

    payload = {"invalid data"}
    response = requests.put(PATH + '/pta/permissions', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid data"}

    # Mock per permission issue
    responses.add(
        responses.PUT,
        f"{PATH}/pta/permissions",
        json={"error": "Permission issue"},
        status=403
    )

    payload = {
        "[object Object]": "second_user",
        "level": "r"
    }
    headers = {
        'Authorization': 'Bearer wrong_token'
    }
    response = requests.put(PATH + '/pta/permissions', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Permission issue"}

    # Mock per document not found
    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id/permissions",
        json={"error": "Document not found"},
        status=404
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id/permissions', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_put_doc_id_entities_e_id():
    # Mock per entity added
    responses.add(
        responses.PUT,
        f"{PATH}/pta/entities/test",
        json={"message": "Entity added successfully"},
        status=201
    )

    payload = {}
    headers = {
       'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/entities/test', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Entity added successfully"}

    # Mock per document non valid
    responses.add(
        responses.PUT,
        f"{PATH}/pta/entities/test",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {"document not valid"}
    response = requests.put(PATH + '/pta/entities/test', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}

    # Mock per document not found
    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id/entities/test",
        json={"error": "Document not found"},
        status=404
    )

    payload = {}
    response = requests.put(PATH + '/wrong_id/entities/test', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_put_doc_id_activities_a_id():
    # Mock per activity added
    responses.add(
        responses.PUT,
        f"{PATH}/pta/activities/test",
        json={"message": "Activity added successfully"},
        status=201
    )

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/activities/test', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Activity added successfully"}

    # Mock per document non valid
    responses.add(
        responses.PUT,
        f"{PATH}/pta/activities/test",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {"document not valid"}
    response = requests.put(PATH + '/pta/activities/test', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}

    # Mock per document not found
    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id/activities/test",
        json={"error": "Document not found"},
        status=404
    )

    payload = {}
    response = requests.put(PATH + '/wrong_id/activities/test', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_put_doc_id_agents_a_id():
    # Mock per agents added
    responses.add(
        responses.PUT,
        f"{PATH}/pta/agents/test",
        json={"message": "Agents added successfully"},
        status=201
    )

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/agents/test', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Agents added successfully"}

    # Mock per document non valid
    responses.add(
        responses.PUT,
        f"{PATH}/pta/agents/test",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {"document not valid"}
    response = requests.put(PATH + '/pta/agents/test', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}

    # Mock per document not found
    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id/agents/test",
        json={"error": "Document not found"},
        status=404
    )

    payload = {}
    response = requests.put(PATH + '/wrong_id/agents/test', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_put_doc_id_relations_r_id():
    # Mock per agents added
    responses.add(
        responses.PUT,
        f"{PATH}/pta/relations/test",
        json={"message": "Relations added successfully"},
        status=201
    )

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/relations/test', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Relations added successfully"}

    # Mock per document non valid
    responses.add(
        responses.PUT,
        f"{PATH}/pta/relations/test",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {"document not valid"}
    response = requests.put(PATH + '/pta/relations/test', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}

    # Mock per document not found
    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id/relations/test",
        json={"error": "Document not found"},
        status=404
    )

    payload = {}
    response = requests.put(PATH + '/wrong_id/relations/test', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_get():
    # Mock per return the list of documents
    responses.add(
        responses.GET,
        PATH,
        json={"documents": []},
        status=200
    )

    response = requests.get(PATH)
    assert response.status_code == 200
    assert response.json() == {"documents": []}

@responses.activate
def test_documents_get_doc_id():
    # Mock per return the correct document
    responses.add(
        responses.GET,
        f"{PATH}/pta",
        json={"document": "pta"},
        status=200
    )

    response = requests.get(PATH + "/pta")
    assert response.status_code == 200
    assert response.json() == {"document": "pta"}

    # Mock per document not found
    responses.add(
        responses.GET,
        f"{PATH}/wrong_id",
        json={"error": "Document not found"},
        status=404
    )

    response = requests.get(PATH + "/wrong_id")
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_get_doc_id_subgraph():
    # Mock per return requested subgraph
    QUERY = "?id=ophidia%3Ahttp%3A%2F%2F127.0.0.1%2Fophidia%2F66%2F7191"
    responses.add(
        responses.GET,
        f"{PATH}/pta/subgraph" + QUERY,
        json={"subgraph": "data"},
        status=200
    )

    response = requests.get(PATH + "/pta/subgraph" + QUERY)
    assert response.status_code == 200
    assert response.json() == {"subgraph": "data"}

    # Mock per document not found
    responses.add(
        responses.GET,
        f"{PATH}/wrong_id/subgraph" + QUERY,
        json={"error": "Document not found"},
        status=404
    )

    response = requests.get(PATH + "/wrong_id/subgraph" + QUERY)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_get_doc_id_entities():
    # Mock per list of entities
    responses.add(
        responses.GET,
        f"{PATH}/pta/entities",
        json={"entities": []},
        status=200
    )

    response = requests.get(PATH + "/pta/entities")
    assert response.status_code == 200
    assert response.json() == {"entities": []}

    # Mock per document not found
    responses.add(
        responses.GET,
        f"{PATH}/wrong_id/entities",
        json={"error": "Document not found"},
        status=404
    )

    response = requests.get(PATH + "/wrong_id/entities")
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_get_doc_id_activities():
    # Mock per list of activities
    responses.add(
        responses.GET,
        f"{PATH}/pta/activities",
        json={"activities": []},
        status=200
    )

    response = requests.get(PATH + "/pta/activities")
    assert response.status_code == 200
    assert response.json() == {"activities": []}

    # Mock per document not found
    responses.add(
        responses.GET,
        f"{PATH}/wrong_id/activities",
        json={"error": "Document not found"},
        status=404
    )

    response = requests.get(PATH + "/wrong_id/activities")
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_get_doc_id_agents():
    # Mock per list of agents
    responses.add(
        responses.GET,
        f"{PATH}/pta/agents",
        json={"agents": []},
        status=200
    )

    response = requests.get(PATH + "/pta/agents")
    assert response.status_code == 200
    assert response.json() == {"agents": []}

    # Mock per document not found
    responses.add(
        responses.GET,
        f"{PATH}/wrong_id/agents",
        json={"error": "Document not found"},
        status=404
    )

    response = requests.get(PATH + "/wrong_id/agents")
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_get_doc_id_entities_e_id():
    # Mock per return requested entity
    responses.add(
        responses.GET,
        f"{PATH}/pta/entities/test",
        json={"entity": "test"},
        status=200
    )

    response = requests.get(PATH + "/pta/entities/test")
    assert response.status_code == 200
    assert response.json() == {"entity": "test"}

    # Mock per document not found
    responses.add(
        responses.GET,
        f"{PATH}/wrong_id/entities/test",
        json={"error": "Document not found"},
        status=404
    )

    response = requests.get(PATH + "/wrong_id/entities/test")
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_get_doc_id_activities_a_id():
    # Mock per list of activities
    responses.add(
        responses.GET,
        f"{PATH}/pta/activities/test",
        json={"activity": "test"},
        status=200
    )

    response = requests.get(PATH + "/pta/activities/test")
    assert response.status_code == 200
    assert response.json() == {"activity": "test"}

    # Mock per document not found
    responses.add(
        responses.GET,
        f"{PATH}/wrong_id/activities/test",
        json={"error": "Document not found"},
        status=404
    )

    response = requests.get(PATH + "/wrong_id/activities/test")
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_get_doc_id_agents_a_id():
    # Mock per list of agents
    responses.add(
        responses.GET,
        f"{PATH}/pta/agents/test",
        json={"agent": "test"},
        status=200
    )

    response = requests.get(PATH + "/pta/agents/test")
    assert response.status_code == 200
    assert response.json() == {"agent": "test"}

    # Mock per document not found
    responses.add(
        responses.GET,
        f"{PATH}/wrong_id/agents/test",
        json={"error": "Document not found"},
        status=404
    )

    response = requests.get(PATH + "/wrong_id/agents/test")
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_get_doc_id_relations_r_id():
    # Mock per list of relations
    responses.add(
        responses.GET,
        f"{PATH}/pta/relations/test",
        json={"relation": "test"},
        status=200
    )

    response = requests.get(PATH + "/pta/relations/test")
    assert response.status_code == 200
    assert response.json() == {"relation": "test"}

    # Mock per document not found
    responses.add(
        responses.GET,
        f"{PATH}/wrong_id/relations/test",
        json={"error": "Document not found"},
        status=404
    )

    response = requests.get(PATH + "/wrong_id/relations/test")
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_documents_delete_doc_id_entities_e_id():
    # Mock per unauthorized delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/entities/test",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer wrong_token'
    }
    response = requests.delete(PATH + '/pta/entities/test', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

    # Mock per successful delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/entities/test",
        json={"message": "Entity deleted successfully"},
        status=200
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/entities/test', headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Entity deleted successfully"}

    # Mock per entity not found
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/entities/test",
        json={"error": "Entity not found"},
        status=404
    )

    response = requests.delete(PATH + '/pta/entities/test', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Entity not found"}

@responses.activate
def test_documents_delete_doc_id_activities_a_id():
    # Mock per unauthorized delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/activities/test",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer wrong_token'
    }
    response = requests.delete(PATH + '/pta/activities/test', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

    # Mock per successful delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/activities/test",
        json={"message": "Activity deleted successfully"},
        status=200
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/activities/test', headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Activity deleted successfully"}

    # Mock per activity not found
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/activities/test",
        json={"error": "Activity not found"},
        status=404
    )

    response = requests.delete(PATH + '/pta/activities/test', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Activity not found"}

@responses.activate
def test_documents_delete_doc_id_agents_a_id():
    # Mock per unauthorized delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/agents/test",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer wrong_token'
    }
    response = requests.delete(PATH + '/pta/agents/test', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

    # Mock per successful delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/agents/test",
        json={"message": "Agent deleted successfully"},
        status=200
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/agents/test', headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Agent deleted successfully"}

    # Mock per agent not found
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/agents/test",
        json={"error": "Agent not found"},
        status=404
    )

    response = requests.delete(PATH + '/pta/agents/test', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Agent not found"}

@responses.activate
def test_documents_delete_doc_id_relations_r_id():
    # Mock per unauthorized delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/relations/test",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer wrong_token'
    }
    response = requests.delete(PATH + '/pta/relations/test', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

    # Mock per successful delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/relations/test",
        json={"message": "Relation deleted successfully"},
        status=200
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/relations/test', headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Relation deleted successfully"}

    # Mock per relation not found
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/relations/test",
        json={"error": "Relation not found"},
        status=404
    )

    response = requests.delete(PATH + '/pta/relations/test', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Relation not found"}

@responses.activate
def test_documents_delete_doc_id():
    # Mock per unauthorized delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer wrong_token'
    }
    response = requests.delete(PATH + '/pta', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

    # Mock per successful delete
    responses.add(
        responses.DELETE,
        f"{PATH}/pta",
        json={"message": "Document deleted successfully"},
        status=200
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta', headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Document deleted successfully"}

    # Mock per document not found
    responses.add(
        responses.DELETE,
        f"{PATH}/pta",
        json={"error": "Document not found"},
        status=404
    )

    response = requests.delete(PATH + '/pta', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}
"""