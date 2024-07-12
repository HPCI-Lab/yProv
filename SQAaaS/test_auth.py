import requests
import test_documents

PATH = "http://localhost:3000/api/v0/auth"

# path to use to create a docker image
# PATH = "http://web:3000/api/v0/auth"



def test_auth_register():
    
    # correct new username and password 
    payload = {
        "user": "myUsername",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 201
    

    # username and password already exist
    payload = {
        "user": "myUsername",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400

    # no username
    payload = {
        "password": "myPassword"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400

    # no password
    payload = {
        "user": "myUsername"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400

    # mi manca l'errore 401

def test_auth_login():
    # correct login
    payload = {
        "user": "myUsername",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 200

    test_documents.TOKEN = response.json().get("result")

    # no username and password
    payload = {
        "user": "",
        "password": ""
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 400

    # correct username, wrong password
    payload = {
        "user": "myUsername",
        "password": "wrongPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401

    # wrong username, correct password
    payload = {
        "user": "wrongUser",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401

    







