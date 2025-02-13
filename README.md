# Provenance as a Service

yProv is a provenance service aimed at addressing multi-level provenance as well as reproducibility challenges in climate analytics experiments. It allows scientists to manage provenance information compliant with the [W3C PROV standard](https://www.w3.org/TR/prov-overview/) in a more structured way and navigate and explore the provenance space across multiple dimensions, thus enabling the possibility to get coarse- or fine-grained information according to the level of interest. 

yProv is a joint project between [University of Trento]:(https://www.unitn.it) and [CMCC](https://www.cmcc.it).

The deployment consists of two Docker containers:
- **yProv** Web Service front-end
- **Neo4J** graph database engine back-end

### Preliminary setup 

- Create a named volume to make Neo4j data persistent
```
docker volume create neo4j_data
```
- Create a named volume to export logs to the host machine
```
docker volume create neo4j_logs
```
- Create a named volume to make yProv configuration and data persistent to the host machine
```
docker volume create yprov_data
```
Create a Docker network to enable communication between the two Docker containers
- Create a Docker network
```
docker network create yprov_net
```

### Deployment from DockerHub

- Run the Neo4j container
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
        -e NEO4J_apoc_export_file_enabled=true \
        -e NEO4J_apoc_import_file_enabled=true \
        -e NEO4J_apoc_import_file_use__neo4j__config=true \
        -e NEO4J_PLUGINS=\[\"apoc\"\] \
        neo4j:enterprise
```
- Run the yProv container
```
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
```

### Deployment from sources

You can also build the yProv image by your own (using the available ```Dockerfile```) and start the two containers.

- Build the yProv image
```
    docker build . -t yprov_web
```
- Run the bash script to start the two containers
```
   ./deploy_service.sh 
```

## yProv CLI
yProv includes a `Command Line Interface` to interact with the service in a more convenient way.
Please refer to [this documentation](https://github.com/HPCI-Lab/yProv-CLI/tree/main) to install the CLI.

## Get started
You can find some ready-to-use examples to get started with yProv under the `examples` folder.

## Advanced options

#### Load Neo4j plugins 
###### Method 1: ```NEO4J_PLUGINS``` utility
You can configure the Neo4j deployment to automatically download and install plugins. The ```NEO4J_PLUGINS``` environment variable can be used to specify the plugins to install.

*Example: Install the APOC Core plugin (```apoc```) and the Graph Data Science plugin (```graph-data-science```)*

You can use the Docker argument 
```
--env NEO4J_PLUGINS='["apoc", "graph-data-science"]'
```

###### Method 2: Installing plugins
To install plugins, including user-defined procedures, mount the folder or volume containing the plugin JARs to ```/plugins```, for example:
```
docker run \
   ...
   -v $HOME/neo4j/plugins:/plugins \
   neo4j:enterprise
```
Neo4j automatically loads any plugins found in the ```/plugins``` folder on startup.

#### Change secret key
A secret key is used to encode/decode the JSON Web Token for user authentication. The default secret key can be overridden by setting the ```SECRET_KEY``` environment variable:
```
    docker run \
        --name web \
        --network=yprov_net \
        -p 3000:3000 \
        -d \
        -v yprov_data:/app/conf \
        --env USER=neo4j \
        --env PASSWORD=password \
        --env SECRET_KEY=my_secret_key \
        hpci/yprov:latest
```
