import responses
import requests

PATH = "http://localhost:3000/api/v0/documents"
TOKEN = "test_token"

@responses.activate
def test_mock_documents_put_doc_id():
    
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

    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {
        "nodes": [
            {
                "id": "1",
                "labels": ["Person"],
                "properties": {
                    # name value should be a string
                    "name": 12345 
                }
            }
        ]     
    }
    response = requests.put(PATH + '/wrong_id', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}


@responses.activate
def test_mock_documents_put_doc_id_permission():
    
    responses.add(
        responses.PUT,
        f"{PATH}/pta/permissions",
        json={"message": "Access added successfully"},
        status=201
    )

    payload = {
        "user": "userB",
        "level": "r"
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/permissions', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Access added successfully"}

    responses.add(
        responses.PUT,
        f"{PATH}/pta/permissions",
        json={"error": "Invalid data"},
        status=400
    )

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/permissions', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid data"}

    responses.add(
        responses.PUT,
        f"{PATH}/pta/permissions",
        json={"error": "Permission issue"},
        status=403
    )

    payload = {
        "user": "userC",
        "level": "r"
    }
    headers = {
        'Authorization': 'Bearer ' + "wrong_token"
    }
    response = requests.put(PATH + '/pta/permissions', json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Permission issue"}
    
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
def test_mock_documents_put_doc_id_entities_e_id():
    
    responses.add(
        responses.PUT,
        f"{PATH}/pta/entities/test",
        json={"message": "Entity added successfully"},
        status=201
    )

    payload = {
        "entity": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  "prov:name": "test"
             }
        }    
    }
    headers = {
       'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/entities/test', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Entity added successfully"}

    responses.add(
        responses.PUT,
        f"{PATH}/pta/entities/test",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {
        "entity": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  # name should be a string
                  "prov:name": 1234
             }
        }    
    }
    headers = {
       'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/entities/test', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}

    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id/entities/test",
        json={"error": "Document not found"},
        status=404
    )

    payload = {
        "entity": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  "prov:name": "test"
             }
        }    
    }
    response = requests.put(PATH + '/wrong_id/entities/test', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}


@responses.activate
def test_mock_documents_put_doc_id_activities_a_id():
    
    responses.add(
        responses.PUT,
        f"{PATH}/pta/activities/test",
        json={"message": "Activity added successfully"},
        status=201
    )

    payload = {
        "activity": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  "prov:name": "test"
             }
        }    
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/activities/test', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Activity added successfully"}

    responses.add(
        responses.PUT,
        f"{PATH}/pta/activities/test",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {
        "activity": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  # name should be a string
                  "prov:name": 1234
             }
        }    
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/activities/test', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}

    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id/activities/test",
        json={"error": "Document not found"},
        status=404
    )

    payload = {
        "activity": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  "prov:name": "test"
             }
        }    
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id/activities/test', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_mock_documents_put_doc_id_agents_a_id():
    
    responses.add(
        responses.PUT,
        f"{PATH}/pta/agents/test",
        json={"message": "Agents added successfully"},
        status=201
    )

    payload = {
        "agent": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  "prov:name": "test"
             }
        }    
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/agents/test', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Agents added successfully"}

    responses.add(
        responses.PUT,
        f"{PATH}/pta/agents/test",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {
        "agent": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  # name should be a string
                  "prov:name": 1234
             }
        }    
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/agents/test', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}

    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id/agents/test",
        json={"error": "Document not found"},
        status=404
    )

    payload = {
        "agent": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  "prov:name": "test"
             }
        }    
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id/agents/test', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}

@responses.activate
def test_mock_documents_put_doc_id_relations_r_id():
    
    responses.add(
        responses.PUT,
        f"{PATH}/pta/relations/test",
        json={"message": "Relations added successfully"},
        status=201
    )

    payload = {
        "relation": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  "prov:name": "test"
             }
        }    
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/relations/test', json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"message": "Relations added successfully"}

    responses.add(
        responses.PUT,
        f"{PATH}/pta/relations/test",
        json={"error": "Document not valid"},
        status=400
    )

    payload = {
        "relation": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  # name should be a string
                  "prov:name": 1234
             }
        }    
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/pta/relations/test', json=payload, headers=headers)
    assert response.status_code == 400
    assert response.json() == {"error": "Document not valid"}

    responses.add(
        responses.PUT,
        f"{PATH}/wrong_id/relations/test",
        json={"error": "Document not found"},
        status=404
    )

    payload = {
        "relation": {
            "ophidia:MyNewTest":
             {
                  "prov:type": "ophidia:datacube",
                  "prov:name": "test"
             }
        }    
    }
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.put(PATH + '/wrong_id/relations/test', json=payload, headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}


@responses.activate
def test_mock_documents_get():
    
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
def test_mock_documents_get_doc_id():
    
    responses.add(
        responses.GET,
        f"{PATH}/pta",
        json={"document": "pta"},
        status=200
    )

    response = requests.get(PATH + "/pta")
    assert response.status_code == 200
    assert response.json() == {"document": "pta"}

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
def test_mock_documents_get_doc_id_subgraph():
    
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
def test_mock_documents_get_doc_id_entities():
    
    responses.add(
        responses.GET,
        f"{PATH}/pta/entities",
        json={"entities": []},
        status=200
    )

    response = requests.get(PATH + "/pta/entities")
    assert response.status_code == 200
    assert response.json() == {"entities": []}

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
def test_mock_documents_get_doc_id_activities():
    
    responses.add(
        responses.GET,
        f"{PATH}/pta/activities",
        json={"activities": []},
        status=200
    )

    response = requests.get(PATH + "/pta/activities")
    assert response.status_code == 200
    assert response.json() == {"activities": []}

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
def test_mock_documents_get_doc_id_agents():
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
def test_mock_documents_get_doc_id_entities_e_id():
    
    responses.add(
        responses.GET,
        f"{PATH}/pta/entities/test",
        json={"entity": "test"},
        status=200
    )

    response = requests.get(PATH + "/pta/entities/test")
    assert response.status_code == 200
    assert response.json() == {"entity": "test"}

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
def test_mock_documents_get_doc_id_activities_a_id():

    responses.add(
        responses.GET,
        f"{PATH}/pta/activities/test",
        json={"activity": "test"},
        status=200
    )

    response = requests.get(PATH + "/pta/activities/test")
    assert response.status_code == 200
    assert response.json() == {"activity": "test"}

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
def test_mock_documents_get_doc_id_agents_a_id():
    
    responses.add(
        responses.GET,
        f"{PATH}/pta/agents/test",
        json={"agent": "test"},
        status=200
    )

    response = requests.get(PATH + "/pta/agents/test")
    assert response.status_code == 200
    assert response.json() == {"agent": "test"}

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
def test_mock_documents_get_doc_id_relations_r_id():

    responses.add(
        responses.GET,
        f"{PATH}/pta/relations/test",
        json={"relation": "test"},
        status=200
    )

    response = requests.get(PATH + "/pta/relations/test")
    assert response.status_code == 200
    assert response.json() == {"relation": "test"}

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
def test_mock_documents_delete_doc_id_entities_e_id():
    
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/entities/test",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer ' + 'wrong_token'
    }
    response = requests.delete(PATH + '/pta/entities/test', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

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

    responses.add(
        responses.DELETE,
        f"{PATH}/pta/entities/test",
        json={"error": "Entity not found"},
        status=404
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/entities/test', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Entity not found"}


@responses.activate
def test_mock_documents_delete_doc_id_activities_a_id():
    
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/activities/test",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer ' + 'wrong_token'
    }
    response = requests.delete(PATH + '/pta/activities/test', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

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

    responses.add(
        responses.DELETE,
        f"{PATH}/pta/activities/test",
        json={"error": "Activity not found"},
        status=404
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/activities/test', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Activity not found"}


@responses.activate
def test_mock_documents_delete_doc_id_agents_a_id():
    
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/agents/test",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer ' + 'wrong_token'
    }
    response = requests.delete(PATH + '/pta/agents/test', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

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

    responses.add(
        responses.DELETE,
        f"{PATH}/pta/agents/test",
        json={"error": "Agent not found"},
        status=404
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/agents/test', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Agent not found"}


@responses.activate
def test_mock_documents_delete_doc_id_relations_r_id():
    
    responses.add(
        responses.DELETE,
        f"{PATH}/pta/relations/test",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer ' + 'wrong_token'
    }
    response = requests.delete(PATH + '/pta/relations/test', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

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

    responses.add(
        responses.DELETE,
        f"{PATH}/pta/relations/test",
        json={"error": "Relation not found"},
        status=404
    )

    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta/relations/test', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Relation not found"}


@responses.activate
def test_mock_documents_delete_doc_id():
    
    responses.add(
        responses.DELETE,
        f"{PATH}/pta",
        json={"error": "Unauthorized"},
        status=403
    )

    headers = {
        'Authorization': 'Bearer ' + 'wrong_token'
    }
    response = requests.delete(PATH + '/pta', headers=headers)
    assert response.status_code == 403
    assert response.json() == {"error": "Unauthorized"}

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

    responses.add(
        responses.DELETE,
        f"{PATH}/pta",
        json={"error": "Document not found"},
        status=404
    )
    headers = {
        'Authorization': 'Bearer ' + TOKEN
    }
    response = requests.delete(PATH + '/pta', headers=headers)
    assert response.status_code == 404
    assert response.json() == {"error": "Document not found"}
