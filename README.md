# Test Suite and SQAaaS

The unit and mock tests are split into two files, auth and documents, respectively, to respect the division of the swagger documentation files. 
To run the tests you need to start Docker Desktop locally and run the command in any folder of the project:
```
pytest
```
or if you want a more detailed output:
```
pytest -v
```

### SQAaaS

Every time a push is made to the SQA branch, the Github Action QAA file is invoked. It automatically starts the SQAaaS platform pipeline and runs mock tests inside it. Unit tests are instead run locally, so it is always necessary to start docker desktop. The file automatically generates the volumes, containers and docker network and removes them once the files have finished running. The file uses the hpci-yprov:mocktest image to run mock tests inside the SQAaaS platform, the dockerfile code is in the hpci-yprov:mocktest folder.

### Future works

The SQAaaS platform is not yet able to handle multi-container architectures like yProv, however it is working on a solution that can include a docker-compose file. This approach has already been implemented and the code is contained in the docker-compose and dockerfile files in the root folder. To run it use the commands:
```
docker-compose build --no-cache
docker-compose up
```
There is also an image that allows you to run both unit tests and mock tests inside a single container and this is contained in the hpci-yprov:1.3 folder.   