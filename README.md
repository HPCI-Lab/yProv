# Provenance as a Service


## Run Docker Containers
- Build service image
```
    docker build . -t prov-rest-neo4j
``` 

- Run service container
```
    docker run\
        --name prov-rest-neo4j \
        -p 7474:7474 -p 7687:7687 -p 3000:3000 \
        -d \
        -v $HOME/neo4j/data:/var/lib/neo4j/data \
        -v $HOME/neo4j/logs:/var/lib/neo4j/logs \
        -v $HOME/neo4j/import:/var/lib/neo4j/import \
        -v $HOME/neo4j/plugins:/var/lib/neo4j/plugins \
        --env NEO4J_AUTH=neo4j/password \
        --env NEO4J_ACCEPT_LICENSE_AGREEMENT=eval \
        --env USER=neo4j \
        --env PASSWORD=password \
        prov-rest-neo4j
```


