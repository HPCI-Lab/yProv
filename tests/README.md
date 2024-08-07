# sqaaas 

The content of this folder aims to evaluate the quality and functioning of the yProv software using the SQAaaS (Software Quality as a Service) platform. The goal is to integrate the execution of unit tests, contained in the test_auth.py and test_documents.py files, within the SQAaaS platform.
Note: all the tests performed in this folder verify the quality and functioning of the yProv software, whose code is contained in the folder [yProv](https://github.com/HPCI-Lab/yProv.git). This folder was imported into this one as a git submodule.


### Run unit tests locally

To run only the unit tests locally, you need to perform the [Preliminary setup](https://github.com/HPCI-Lab/yProv?tab=readme-ov-file#preliminary-setup) and [Deployment from DockerHub](https://github.com/HPCI-Lab/yProv?tab=readme-ov-file#deployment-from-dockerhub) points described in the Readme file of the folder [yProv](https://github.com/HPCI-Lab/yProv.git). Once the containers have been created it is necessary to update the yProv submodule, so that the content corresponds to the code of the original folder:

```
cd yProv
git checkout main  
git pull origin main
```

to run tests:

```
python3 -m pytest -v 
```


### Quality Assessment & Awarding v1

This is an intermediate step for integrating unit tests into the SQAaaS platform. The [Quality_Assessment_&_Awarding_v1](https://github.com/HPCI-Lab/sqaaas/blob/main/.github/workflows/Quality_Assessment_%20%26_Awarding_v1.yml) file corresponds to a github action that is triggered at each push event. The SQAaaS platform tests the quality of the yProv software while the unit tests for the operation of the yProv API are performed locally.


### Quality Assessment & Awarding v2

The [Quality_Assessment_&_Awarding_v2](https://github.com/HPCI-Lab/sqaaas/blob/main/.github/workflows/Quality_Assessment_%20%26_Awarding_v1.yml) file corresponds to a new github action, also triggered by each push event, and allows the SQAaaS platform to execute all tests. To integrate unit tests into the SQAaaS platform, the latter requires a docker image on which to build a container in which to run the tests. Currently this module is not functional, however it is possible to create a local docker image to test the correct functioning of the unit tests within the container.

To create the image you need to modify the PATH variable contained in the auth and documents files, commenting the current variable and uncommenting the commented PATH variable below. Then you need to push the changes to the github folder. Now you can create the image and run the container:

```
docker build -t sqaaas_yprov:v1.0 .
docker run --name unittests --privileged -v /var/run/docker.sock:/var/run/docker.sock sqaaas_yprov:v1.0
```

Note: Currently, if the containers described in [Run unit tests locally](https://github.com/HPCI-Lab/sqaaas?tab=readme-ov-file#run-unit-tests-locally) point have already been created locally, to run the container it is necessary to temporarily delete them.






