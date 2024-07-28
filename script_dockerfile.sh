#!/bin/bash

# Avvia i servizi definiti in docker-compose.yml
docker-compose -f /app/docker-compose.yml up -d

# Monitoraggio della prontezza dei servizi
echo "Attendi che Neo4j sia pronto..."
for i in {1..30}; do
    if curl -s http://localhost:7474 > /dev/null; then
        echo "Neo4j è pronto!"
        break
    fi
    echo "Tentativo $i/30: Neo4j non è pronto"
    sleep 10
done

echo "Attendi che l'API di yProv sia pronta..."
for i in {1..30}; do
    if curl -s http://localhost:3000/api/v0/documents > /dev/null; then
        echo "API di yProv è pronta!"
        break
    fi
    echo "Tentativo $i/30: API non è pronta"
    sleep 10
done

# Se è passato l'argomento "test", esegui i test
if [[ "$1" == "test" ]]; then
    echo "Esecuzione dei test..."
    pytest -v
fi
