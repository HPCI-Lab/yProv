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

-------

## yProv Command Line Interface (CLI)

The yProv CLI provides a set of commands, which are basically Python wrappers to the RESTful API calls designed for the yProv service.

Five classes of resources have been identified, namely document, entity, activity, agent and relation. For each, it is possible to perform the CRUD operations: Create, Read, Update, Delete.

The generic usage is:
```
flask RESOURCE COMMAND [ARGS]
```

where RESOURCE = ["activities", "agents", "documents", "elements", "entities", "relations"]
and COMMAND = ["create","delete","get","update"]

To get further information about a specific resource (e.g., documents) and command (e.g., get), you can simply run

```
flask documents get --help
```

Here is the full list of available commands and how to use them. 

### Documents
- Get all documents
```
flask doguments get
```
- Get document
```
flask documents get -doc_id <doc-id>
```
  
- Create document
```
flask documents create <doc-id> <file.json>
```

- Delete document
```
flask documents delete <doc-id>
```

### Activities
- Get activity
```
flask activities get <doc-id> <el-id>
```
- Create activity
```
flask activities create <doc-id> <file.json>
```
- Update activity
```
flask activities update <doc-id> <el-id> <file.json>
```
- Delete activity
```
flask activities delete <doc-id> <el-id>
```

### Agents
- Get agent
```
flask agents get <doc-id> <el-id>
```
- Create agent
```
flask agents create <doc-id> <file.json>
```
- Update agent
```
flask agents update <doc-id> <el-id> <file.json>
```
- Delete agent
```
flask agents delete <doc-id> <el-id>
```

### Elements
- Get element
```
flask elements get <doc-id> <el-id>
```
- Create element
```
flask elements create <doc-id> <file.json>
```
- Update element
```
flask elements update <doc-id> <el-id> <file.json>
```
- Delete element
```
flask elements delete <doc-id> <el-id>
```

### Entities
- Get entity
```
flask entities get <doc-id> <el-id>
```
- Create entity
```
flask entities create <doc-id> <file.json>
```
- Update entity
```
flask entities update <doc-id> <el-id> <file.json>
```
- Delete entity
```
flask entities delete <doc-id> <el-id>
```

### Relations
- Get relation
```
flask relations get <doc-id> <rel-id>
```
- Create relation
```
flask relations create <doc-id> <file.json>
```
- Update relation
```
flask relations update <doc-id> <rel-id> <file.json>
```
- Delete relation
```
flask relations delete <doc-id> <rel-id>
```
