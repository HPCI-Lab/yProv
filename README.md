# Provenance as a Service

## Run with Docker Compose
- Buil compose image
```
    docker-compose build
```

- Run compose containers
```
    docker-compose up -d
```

## Run on two Docker Containers
- Build service image
```
    docker build . -t prov-rest-neo4j
``` 

- Run neo4j container
```
    docker run \
        --name neo4j \
        -p 7474:7474 -p7687:7687 \
        -d \
        -v $HOME/neo4j/data:/data \
        -v $HOME/neo4j/logs:/logs \
        -v $HOME/neo4j/import:/var/lib/neo4j/import \
        -v $HOME/neo4j/plugins:/plugins \
        --env NEO4J_AUTH=neo4j/password \
        --env NEO4J_ACCEPT_LICENSE_AGREEMENT=eval \
        neo4j:enterprise
```

- Run service container
```
    docker run \
        --name prov-rest \
        -p 3000:3000 \
        -d \
        prov-rest-neo4j
```


