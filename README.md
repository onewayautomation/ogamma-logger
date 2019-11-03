# *ogamma* Visual Logger for OPC

*ogamma* Visual Logger for OPC is an integration tool to:
* **Collect** data from OPC UA Servers;
* **Store** that data in TimescaleDB (PostgreSQL database optimized to store time-series data). Regular version of PostgreSQL can be used too.
* **Visualize** data using Grafana, acting as a REST back-end for its SimpleJson data source plugin. It can fetch real time or historical data directly from OPC UA Servers, or from PostgreSQL.
* **Analyze** data using SQL queries.
Each instance of *ogamma* Visual Logger can implement only one role or all of them.

Multiple instances can run in parallel in different roles, making horizontal scaling easy.

Note that to enable all the features third party components are required.  The easiest way to setup and run *ogamma* Visual Logger and dependency services is to use Docker images, which can be easily pulled and then started with single command ``docker-compose up``, by using of the ``docker-compose.yml`` file which is available at this repository: https://github.com/onewayautomation/ogamma-logger/blob/master/docker/docker-compose.yml

# Context Diagram
![*ogamma* Visual Logger - Context Diagram](https://raw.githubusercontent.com/onewayautomation/ogamma-logger/master/ContextDiagram.png)

# Getting Started with Docker image.

Docker image is available at: https://hub.docker.com/r/ogamma/logger.

File ``docker/docker-compose.yml`` allows to pull *ogamma* Visual Logger image and additionally all required dependency images:
* Database (TimescaleDB);
* PgAdmin, to manage database;
* Grafana, optional, to visualize data;
* Sample OPC UA Server from Microsoft.

## Prerequisites.

There is only one: Docker Desktop, available to download here https://www.docker.com/products/docker-desktop. It can be installed in Windows as well as in Linux machines.

## To setup all service components and run them:

* Pull file ``docker/docker-compose.yml`` from this repository;
* Open shell terminal (PowerShell on Windows, or bash in Linux);
* Navigate to the folder where docker-compose.yml is located;
* Run command ``docker-compose up``.

This command will pull all images from Docker Hub (and might take few or more minutes, but this step happens only once, then you run this command at the very first time), and start all required services.

After that:
* Web GUI for *ogamma* Visual Logger will be available at http://localhost:4880;
* Database TimescaleDB - at localhost:5432. (Default user credentials can be found in docker-compose.yml file).
* PgAdmin - at http://localhost:4888;
* Grafana - at http://localhost:3000

# Distribution packages for Windows and Linux (Ubuntu 18.04 and Debian  Stretch).

For links to download installation packages please refer to section ``Deploy`` of the online User Manual: https://onewayautomation.com/visual-logger-docs/html/deploy.html

# User Manual

For more information, please refer to online User Manual available at https://onewayautomation.com/visual-logger-docs/html/index.html


Introduction video with more detailed instructions is available on youtube at https://youtu.be/yZdsyVz7hw0 (for older version, needs update).