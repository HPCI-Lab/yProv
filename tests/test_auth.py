import requests
import test_documents


PATH = "http://localhost:3000/api/v0/auth"

# path to use to create a docker image
#PATH = "http://web:3000/api/v0/auth"



def test_auth_register():
    
    """
    # correct new username and password 
    payload = {
        "user": "userA",
        "password": "userA"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 201

     # correct new username and password 
    payload = {
        "user": "userB",
        "password": "userB"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 201
    """
    
    # username and password already exist
    payload = {
        "user": "userA",
        "password": "userA"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400

    # no username
    payload = {
        "password": "userA"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400

    # no password
    payload = {
        "user": "userA"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400


def test_auth_login():
    # Login corretto
    payload = {
        "user": "userA",
        "password": "userA"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 200

    test_documents.TOKEN_A = response.json().get("result")

    # Login corretto
    payload = {
        "user": "userB",
        "password": "userB"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 200

    test_documents.TOKEN_B = response.json().get("result")

    # Login senza username e password
    payload = {
        "user": "",
        "password": ""
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 400

    # Login con username corretto e password errata
    payload = {
        "user": "userA",
        "password": "wrongPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401

    # Login con username errato e password corretta
    payload = {
        "user": "wrongUser",
        "password": "userA"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401
