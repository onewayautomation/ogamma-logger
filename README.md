# *ogamma* Visual Logger for OPC

*ogamma* Visual Logger for OPC is an integration tool to:
* **Collect** data from OPC UA Servers, as well as from classic OPC DA servers using additional wrapper application;
* **Store** that data in time-series database:
  * ``TimescaleDB`` (PostgreSQL database optimized to store time-series data);
  * ``PostgreSQL`` regular version;
  * ``InfluxDB`` (versions 1.7 or 2.0);
  * ``Apache Kafka``.
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
* Databases (TimescaleDB, InfluxDB versions 1.7 and 2.0, Apache Kafka);
* PgAdmin, to manage database PostgreSQL;
* Grafana, optional, to visualize data;
* Sample OPC UA Server from Microsoft.

## Prerequisites.

There is only one: Docker Desktop, available to download here https://www.docker.com/products/docker-desktop. It can be installed in Windows as well as in Linux machines.

## To setup all service components and run them:

* Pull this repository to some local folder;
* Open shell terminal (PowerShell on Windows, or bash in Linux);
* Navigate to the folder ``docker`` where file ``docker-compose.yml`` is located;
* Run command ``docker-compose up``.

All container images from Docker Hub will be pulled (this might take few or more minutes, but this step happens only once, when you run this command at the very first time), and all required services will be started.

After that:
* Web GUI for *ogamma* Visual Logger will be available at http://localhost:4880;
* Database TimescaleDB - at localhost:5432. (Default user credentials can be found in docker-compose.yml file).
* PgAdmin - at http://localhost:4888;
* Grafana - at http://localhost:3000
* InfluxDB v 2.0 - at http://localhost:9999
* InfluxDB v 1.7 - at localhost:8086.
* Apache Kafka - at localhost:9092

By default, TimescaleDB is used as timeseries database. In order to use InfluxDB or Kafka, configuration file should be modified accordingly.

# Distribution packages for Windows and Linux (Ubuntu 18.04 and Debian  Stretch).

For links to download installation packages please refer to section ``Deploy`` of the online User Manual: https://onewayautomation.com/visual-logger-docs/html/deploy.html

# User Manual

For more information, please refer to online User Manual available at https://onewayautomation.com/visual-logger-docs/html/index.html

You can see Visual Logger in action in youtube video at https://www.youtube.com/watch?v=mY9Wh8wAKZg&t=215s, where it is used to explain OPC UA terms such as publishing interval, sampling interval and queue size for monitored items.

Introduction video with more detailed instructions is available on youtube at https://youtu.be/yZdsyVz7hw0 (for older version, needs update).
