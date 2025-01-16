import responses
import requests

PATH = "http://localhost:3000/api/v0/auth"

@responses.activate
def test_mock_auth_register():
    
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
def test__mock_auth_login():
    
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
