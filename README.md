# Provenance as a Service


## Run Docker Containers
- Build service image
```
    docker build . -t yprov_single_instance
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
- Run service container by mounting the two named volumes to the default file locations
```
    docker run\
        --name yprov_neo4j_instance \
        -p 7474:7474 -p 7687:7687 -p 3000:3000 \
        -d \
        --volume neo4j_data:/var/lib/neo4j/ \
        --volume neo4j_logs:/var/log/neo4j/ \
        --volume yprov_data:/app/conf
        --env USER=neo4j \
        --env PASSWORD=password \
        yprov_single_instance
```
- If you need to restart the container due to some errors that caused the container to exits please use only the last command 
