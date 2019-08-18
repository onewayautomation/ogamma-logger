# *ogamma* Visual Logger for OPC

*ogamma* Visual Logger for OPC is an integration tool, which performs 2 tasks:

* Collects data from OPC UA Servers and stores it in TimescaleDB (PostgreSQL database optimized to store time-series data). Regular version of PostgreSQL can be used too.

* Acts as a back-end for Grafana SimpleJson data source plugin. It can fetch data directly from OPC UA Servers, or from PostgreSQL. 

Each instance of *ogamma* Visual Logger can implement both tasks, or only one of them.

Note that to enable all the features third party components are required.  The easiest way to setup and run *ogamma* Visual Logger and dependency services is to use Dockaer images, which can be easily pulled and then started with single command ``docker-compose up``, by using of the ``docker-compose.yml`` file which is available at this repository: https://github.com/onewayautomation/ogamma-logger/blob/master/docker/docker-compose.yml

# Context Diagram
![*ogamma* Visual Logger - Context Diagram](https://raw.githubusercontent.com/onewayautomation/ogamma-logger/master/ContextDiagram.png)

# Getting Started with Docker image.

Docker image is available at: https://cloud.docker.com/u/ogamma/repository/docker/ogamma/logger.

File ``docker/docker-compose.yml`` allows to pull *ogamma* Visual Logger image and additionally all required dependency images:
* Database (TimescaleDB);
* PgAdmin, to manage database;
* Grafana, optional, to visualize data;
* Sample OPC UA Server from Microsoft.

## Prerequisites.

There is only one: Docker Desktop, available to download here https://www.docker.com/products/docker-desktop. It can be installed in Windows as well as in Linux machines.

## To setup all service components and run them:

* Pull file ``docker/docker-compose.yml`` from this repository;
* Open shell terminal (PowerShell on Windoes, or bash in Linux);
* Navigate to the folder where docker-compose.yml is located;
* Run command ``docker-compose up``.

This command will pull all images from Docker Hub (and might take few or more minutes, but this step happens only once, then you run this command at the very first time), and start all required services.

After that:
* Web GUI for *ogamma* Visual Logger will be available at http://localhost:4880;
* Database TimescaleDB - at localhost:5432. (Default user credentials can be found in docker-compose.yml file).
* PgAdmin - at http://localhost:80;
* Grafana - at https://localhost:3000

# Distribution packages for Windows and Linux Ubuntu 18.04

For links to donwload installation packages please refer to section ``Deploy`` of the online User Manual: https://onewayautomation.com/visual-logger-docs/html/deploy.html

# User Manual

For more information, please refer to online User Manual available at https://onewayautomation.com/visual-logger-docs/html/index.html


Introduction video with more detailed instructions is available on youtube at https://youtu.be/yZdsyVz7hw0 (for older version, needs update).