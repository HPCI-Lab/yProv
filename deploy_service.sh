#!/bin/bash

#docker volume create neo4j_data
#docker volume create neo4j_logs
#docker volume create yprov_data
#docker network create yprov_net

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
        -e NEO4J_PLUGINS=\[\"apoc\"\] \
        neo4j:enterprise

docker run \
        --restart on-failure \
        --name web \
        --network=yprov_net \
        -p 3000:3000 \
        -d \
        -v yprov_data:/app/conf \
        --env USER=neo4j \
        --env PASSWORD=password \
        -e CLIENT_ID=<prov_client_id> \
        -e CLIENT_SECRET=<prov_client_secret> \
	-e REQUIRED_ENTITLEMENTS=\[\"urn:mace:egi.eu:group:enes.pilot.eosc-beyond.eu:role=member#aai.egi.eu\"\] \
        -e INTROSPECTION_ENDPOINT=https://enes-proxy.pilot.eosc-beyond.eu/auth/realms/enes/protocol/openid-connect/token/introspect \
        yprov_web
