#!/bin/bash
set -e

# Create Docker volumes if not exist
for volume in neo4j_data neo4j_logs yprov_data; do
  if [ "$(docker volume ls -q -f name=$volume)" == "" ]; then
    docker volume create $volume
  fi
done

# Remove and recreate Docker network if it exists
if [ "$(docker network ls -q -f name=yprov_net)" != "" ]; then
  docker network rm yprov_net
fi
docker network create yprov_net

# Run Neo4j (db) container
docker run \
  --name db \
  --network=yprov_net \
  -p 7474:7474 -p 7687:7687 \
  -d \
  -v neo4j_data:/data \
  -v neo4j_logs:/logs \
  -v $HOME/neo4j/import:/var/lib/neo4j/import \
  -v $HOME/neo4j/plugins:/plugins \
  --env NEO4J_AUTH=neo4j/password \
  --env NEO4J_ACCEPT_LICENSE_AGREEMENT=eval \
  -e NEO4J_apoc_export_file_enabled=true \
  -e NEO4J_apoc_import_file_enabled=true \
  -e NEO4J_apoc_import_file_use__neo4j__config=true \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:enterprise

# Run yProv (web) container
docker run \
  --restart on-failure \
  --name web \
  --network=yprov_net \
  -p 3000:3000 \
  -d \
  -v yprov_data:/app/conf \
  --env USER=neo4j \
  --env PASSWORD=password \
  hpci/yprov:latest

# Get the current container's hostname (which is the container's ID)
CONTAINER_ID=$(cat /etc/hostname)

# Connect the current container to the yprov_net network
docker network connect yprov_net "$CONTAINER_ID"

# Try to connect to Neo4j
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

echo "Ready to perform tests"

# Keep the container running
tail -f /dev/null




