"""

import pytest
import subprocess
import time
import requests
import os

# URL dell'API
PATH = "http://localhost:3000/api/v0/auth"

@pytest.fixture(scope='session', autouse=True)
def setup_docker_environment():
    # Crea volumi Docker
    subprocess.run(["docker", "volume", "create", "neo4j_data"], check=True)
    subprocess.run(["docker", "volume", "create", "neo4j_logs"], check=True)
    subprocess.run(["docker", "volume", "create", "yprov_data"], check=True)

    # Crea rete Docker, ignorando l'errore se la rete esiste già
    try:
        subprocess.run(["docker", "network", "create", "yprov_net"], check=True)
    except subprocess.CalledProcessError as e:
        if "already exists" in str(e.stderr):
            pass
        else:
            raise

    # Avvia il container Neo4j senza i volumi di import e plugins
    subprocess.run([
        "docker", "run", "--name", "db", "--network=yprov_net",
        "-p", "7474:7474", "-p", "7687:7687", "-d",
        "-v", "neo4j_data:/data",
        "-v", "neo4j_logs:/logs",
        "--env", "NEO4J_AUTH=neo4j/password",
        "--env", "NEO4J_ACCEPT_LICENSE_AGREEMENT=eval",
        "-e", "NEO4J_apoc_export_file_enabled=true",
        "-e", "NEO4J_apoc_import_file_enabled=true",
        "-e", "NEO4J_apoc_import_file_use__neo4j__config=true",
        "-e", "NEO4J_PLUGINS=['apoc']",
        "neo4j:enterprise"
    ], check=True)

    # Avvia il container API
    subprocess.run([
        "docker", "run", "--restart", "on-failure", "--name", "web", "--network=yprov_net",
        "-p", "3000:3000", "-d",
        "-v", "yprov_data:/app/conf",
        "--env", "USER=neo4j",
        "--env", "PASSWORD=password",
        "hpci/yprov:latest"
    ], check=True)

    # Attende che l'API sia pronta
    max_attempts = 30
    attempt = 0
    while attempt < max_attempts:
        try:
            response = requests.get("http://localhost:3000/api/v0/documents")
            if response.status_code == 200:
                print("API is ready!")
                break
        except requests.exceptions.RequestException:
            pass
        attempt += 1
        print(f"Attempt {attempt}/{max_attempts}: API is not ready yet. Waiting...")
        time.sleep(10)

    yield

    # Cleanup dei container e volumi Docker
    subprocess.run(["docker", "rm", "-f", "web"], check=True)
    subprocess.run(["docker", "rm", "-f", "db"], check=True)
    subprocess.run(["docker", "network", "rm", "yprov_net"], check=True)
    subprocess.run(["docker", "volume", "rm", "neo4j_data"], check=True)
    subprocess.run(["docker", "volume", "rm", "neo4j_logs"], check=True)
    subprocess.run(["docker", "volume", "rm", "yprov_data"], check=True)

def test_auth_register():
    # Registrazione con nuovo username e password
    payload = {
        "user": "myUsername",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 201

    # Registrazione con username e password già esistenti
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400

    # Registrazione senza username
    payload = {
        "password": "myPassword"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400

    # Registrazione senza password
    payload = {
        "user": "myUsername"
    }
    response = requests.post(PATH + '/register', json=payload)
    assert response.status_code == 400

def test_auth_login():
    # Login corretto
    payload = {
        "user": "myUsername",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 200

    #test_documents.TOKEN = response.json().get("result")

    # Login senza username e password
    payload = {
        "user": "",
        "password": ""
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 400

    # Login con username corretto e password errata
    payload = {
        "user": "myUsername",
        "password": "wrongPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401

    # Login con username errato e password corretta
    payload = {
        "user": "wrongUser",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401

"""

import requests


#PATH = "http://localhost:3000/api/v0/auth"

# path to use to create a docker image
PATH = "http://web:3000/api/v0/auth"



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


def test_auth_login():
    # Login corretto
    payload = {
        "user": "myUsername",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 200

    #test_documents.TOKEN = response.json().get("result")

    # Login senza username e password
    payload = {
        "user": "",
        "password": ""
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 400

    # Login con username corretto e password errata
    payload = {
        "user": "myUsername",
        "password": "wrongPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401

    # Login con username errato e password corretta
    payload = {
        "user": "wrongUser",
        "password": "myPassword"
    }
    response = requests.post(PATH + '/login', json=payload)
    assert response.status_code == 401
