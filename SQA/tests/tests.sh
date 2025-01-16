#!/bin/bash

echo "Connection to Neo4j"
for i in {1..15}; do
    if curl -s http://db:7474 > /dev/null; then
        echo "Neo4j is ready!"
        break
    fi
    echo "Attempt $i/15: Neo4j is not ready"
    sleep 10
done

# Try to connect to yProv API
echo "Connection to yProv API"
for i in {1..15}; do
    if curl -s http://web:3000/api/v0/documents > /dev/null; then
        echo "API is ready!"
        break
    fi
    echo "Attempt $i/15: API is not ready"
    sleep 10
done

pytest -v tests/