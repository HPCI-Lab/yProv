import pytest
import responses
import requests

# URL dell'API
PATH = "http://localhost:3000/api/v0/auth"

@responses.activate
def test_auth_register():
    # Mock per la registrazione con nuovo username e password
    responses.add(
        responses.POST,
        f"{PATH}/register",
        json={"message": "User created successfully"},
        status=201
    )

    payload = {
        "user": "myUsername",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}

    # Mock per la registrazione con username e password già esistenti
    responses.add(
        responses.POST,
        f"{PATH}/register",
        json={"message": "User already exists"},
        status=400
    )

    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "User already exists"}

    # Mock per la registrazione senza username
    responses.add(
        responses.POST,
        f"{PATH}/register",
        json={"message": "Username is required"},
        status=400
    )

    payload = {
        "password": "myPassword"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Username is required"}

    # Mock per la registrazione senza password
    responses.add(
        responses.POST,
        f"{PATH}/register",
        json={"message": "Password is required"},
        status=400
    )

    payload = {
        "user": "myUsername"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Password is required"}

@responses.activate
def test_auth_login():
    # Mock per il login corretto
    responses.add(
        responses.POST,
        f"{PATH}/login",
        json={"token": "fake-jwt-token"},
        status=200
    )

    payload = {
        "user": "myUsername",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 200
    assert response.json() == {"token": "fake-jwt-token"}

    # Mock per il login senza username e password
    responses.add(
        responses.POST,
        f"{PATH}/login",
        json={"message": "Username and password are required"},
        status=400
    )

    payload = {
        "user": "",
        "password": ""
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 400
    assert response.json() == {"message": "Username and password are required"}

    # Mock per il login con username corretto e password errata
    responses.add(
        responses.POST,
        f"{PATH}/login",
        json={"error": "Please register!"},
        status=401
    )

    payload = {
        "user": "myUsername",
        "password": "wrongPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401
    assert response.json() == {"error": "Please register!"}

    # Mock per il login con username errato e password corretta
    responses.add(
        responses.POST,
        f"{PATH}/login",
        json={"error": "Please register!"},
        status=401
    )

    payload = {
        "user": "wrongUser",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401
    assert response.json() == {"error": "Please register!"}
