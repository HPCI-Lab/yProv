#!/bin/bash
set -e

log() {
    echo "$(date) - $1"
}

cleanup() {
    log "Clean up container, volumes, and network"
    docker stop web || true
    docker stop db || true
    docker rm web || true
    docker rm db || true
    docker volume rm neo4j_data || true
    docker volume rm neo4j_logs || true
    docker volume rm yprov_data || true
    docker network disconnect yprov_net "$CONTAINER_ID" || true
    docker network rm yprov_net || true
}

# Set trap to execute cleanup on exit
trap cleanup EXIT

log "Removing and recreating Docker volumes"
for volume in neo4j_data neo4j_logs yprov_data; do
  if [ "$(docker volume ls -q -f name=$volume)" != "" ]; then
    docker volume rm $volume
  fi
  docker volume create $volume
done

log "Removing and recreating Docker network"
if [ "$(docker network ls -q -f name=yprov_net)" != "" ]; then
  docker network rm yprov_net
fi
docker network create yprov_net

log "Starting Neo4j (db) container"
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

log "Starting yProv (web) container"
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

CONTAINER_ID=$(cat /etc/hostname)
docker network connect yprov_net "$CONTAINER_ID"

log "Connecting to Neo4j"
for i in {1..30}; do
    if curl -s http://db:7474 > /dev/null; then
        log "Neo4j is ready!"
        break
    fi
    log "Attempt $i/30: Neo4j is not ready"
    sleep 10
done

log "Connecting to yProv API"
for i in {1..30}; do
    if curl -s http://web:3000/api/v0/documents > /dev/null; then
        log "API is ready!"
        break
    fi
    log "Attempt $i/30: API is not ready"
    sleep 10
done

if [[ "$1" == "test" ]]; then
    log "Starting tests"
    python3 -m pytest -v 2>&1 | tee -a >(log)
fi
