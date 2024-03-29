# Provenance as a Service

## Run with Docker Compose
- Buil compose image
```
    docker compose build
```

- Run compose containers
```
    docker compose up -d
```

## Run on two Docker Containers
- Build service image
```
    docker build . -t yprov-web
```
- Create a named volume to make Neo4j data persistent
```
docker volume create neo4j_data
```
- Create a named volume to export logs to the host machine
```
docker volume create neo4j_logs
```
- Create a named volume to make the configuration of yprov persistent to the host machine
```
docker volume create yprov_data
```
The volumes definition is necessary only on the first start (or if the volumes are deleted)
- Create a Docker network
```
docker network create yprov_net
```
- Run neo4j container
```
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
        neo4j:enterprise
```

- Run service container
```
    docker run \
        --name web \
        --network=yprov_net \
        -p 3000:3000 \
        -d \
        -v yprov_data:/app/conf \
        --env USER=neo4j \
        --env PASSWORD=password \
        yprov-web
```
