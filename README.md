# *ogamma* Visual Logger for OPC

*ogamma* Visual Logger for OPC is an integration tool to:
* **Collect** data from OPC UA Servers, as well as from classic OPC DA servers using additional wrapper application;
* **Store** that data in time-series database:
  * ``TimescaleDB`` (PostgreSQL database optimized to store time-series data);
  * ``PostgreSQL`` regular version;
  * ``InfluxDB`` (versions 1.7, 1.8 or 2.x);
  * ``Confluent: Cloud and Enterprise``;
  * ``Apache Kafka``;
  * ``Microsoft SQL Server``;
  * ``MySQL``;
  * ``SQLite``;
  * ``MQTT Brokers``. Using MQTT protocol, data can be published to any Cloud/IoT platform providing access over MQTT such as:
    * Generic MQTT broker (for example, Eclipse Mosquito).
    * Microsoft Azure IoT Hub;
    * AWS IoT Broker;
    * Google Cloud IoT Core MQTT Bridge;

* **Visualize** data using Grafana, acting as a REST back-end for its SimpleJson data source plugin. It can fetch real time or historical data directly from OPC UA Servers, or from PostgreSQL.
* **Analyze** data using query language (specific to type of the used TSDB).

Each instance of *ogamma* Visual Logger can implement only one role or all of them.

Multiple instances can run in parallel in different roles, making horizontal scaling easy.

Note that to enable all the features third party components are required.  The easiest way to setup and run *ogamma* Visual Logger and dependency services is to use Docker images, which can be easily pulled and then started with single command ``docker-compose up``, by using of the ``docker-compose.yml`` file which is available at this repository: https://github.com/onewayautomation/ogamma-logger/blob/master/docker/docker-compose.yml Note that .yml files have specific version numbers of images. If you have containers running older versions of images, after updating of .yml files they might stop working due to issues with upgrading of data volumes. 

# Context Diagram
![*ogamma* Visual Logger - Context Diagram](https://onewayautomation.com/wp-content/uploads/VisualLoggerContextDiagram2.png)

# Getting Started with Docker image.

Docker image is available at: https://hub.docker.com/r/ogamma/logger.

File ``docker/docker-compose.yml`` allows to pull *ogamma* Visual Logger image. The folder ``docker`` has also .yml files for other images (time-series databases), that can be started independently, by passing file name in the command ``docker compose -f <file-name> ``:
* Time-series databases (TimescaleDB, InfluxDB versions 1.x and 2.x);
* Confluent / Apache Kafka;
* PgAdmin, to manage database PostgreSQL;
* Grafana, optional, to visualize data;
* Sample OPC UA Server from Microsoft.
* MQTT brocker.

## Prerequisites.

There is only one: Docker Desktop, available to download here https://www.docker.com/products/docker-desktop. It can be installed in Windows as well as in Linux machines.

## To setup all service components and run them:

* Pull this repository to some local folder;
* Open shell terminal (PowerShell on Windows, or bash in Linux);
* Navigate to the folder ``docker`` where file ``docker-compose.yml`` is located;
* Run command ``docker-compose up -d``.
* To start other containers, pass yml file name. For example, to start InfluxDB version 1.8, run command: ``docker compose -f influxdb.yml up -d``.

The container image from Docker Hub will be pulled (this might take few or more minutes, but this step happens only once, when you run this command at the very first time), and service(s) defined in the yml file will be started.

After that:
* Web GUI for *ogamma* Visual Logger will be available at http://localhost:4880;

If you start also other services, they will be available at following below URLs:
* Database TimescaleDB - at localhost:5432. (Default user credentials can be found in file timescaledb.yml).
* PgAdmin - at http://localhost:4888;
* Grafana - at http://localhost:3000
* InfluxDB v 2.x - at http://localhost:8086
* InfluxDB v 1.x - at http://localhost:8084.
* Apache Kafka - at http://localhost:9092
* Confluent Control Center - at http://localhost:9021

Note that before starting containers using file ``confluent.yml``, download the OPC UA Kafka Source Connector jar file https://onewayautomation.com/opcua-binaries/OpcUaKafkaSourceConnector-1.0.0-4.2.2.jar/OpcUaKafkaSourceConnector-1.0.0-4.2.2.jar to the folder ``docker/custom-connectors``.

To log data from OPC UA Servers to the specific database, the instance of the ogamma Visual Logger for OPC application needs to be configured. Refer to the online User Manual for details: https://onewayautomation.com/visual-logger-docs/html/

## Docker-compose files to demo High Availability feature

To run 2 instances of the *ogamma* Visual Logger as a member nodes of the High Availability cluster, use docker-compose configuration files ``docker-compose-ha-node-1.yml`` and ``docker-compose-ha-node-2.yml`` respectevely for the node 1 and node 2. 

Note: to configure the application with support of this feature, the application should be installed in 2 instances, both using the same configuration database. Then they both should be configured to use the same ``Collector Configuration`` and the same time-series database in the ``Instance Settings`` dialog window. One of them will be in ``Active`` mode, that is, collecting data from OPC UA Servers. The second stays in  ``Standby`` mode. Using new service HA Node Manager, these nodes shell be communicating with each other, and publishing information about current state of a node periodically. At the same time this service calls new endpoint ``/health`` in the application GUI endpoint to check its state. Based on that state, the node decides if it is expected to be ``Active``, or ``Standby``. If both nodes are healthy, the node with highest priority becomes active. If the active node has issues, second node becomes active. This allows continious data flow with minimal interruption during the failover period: about 2 seconds.

For more details about configuration of the application to run in a High Availability cluster, refer this YouTube video: https://youtu.be/ND5PoKYOgc4

# Distribution packages for Windows and Linux.

For links to download installation packages please refer to section ``Deploy`` of the online User Manual: https://onewayautomation.com/visual-logger-docs/html/deploy.html

# User Manual

For more information, please refer to online User Manual available at https://onewayautomation.com/visual-logger-docs/html/index.html

You can see Visual Logger in action in youtube video at https://www.youtube.com/watch?v=mY9Wh8wAKZg&t=215s, where it is used to explain OPC UA terms such as publishing interval, sampling interval and queue size for monitored items.

Introduction video with more detailed instructions is available on youtube at https://youtu.be/yZdsyVz7hw0 (for older version, needs update).

# Breaking change in Docker container version 4.2.0

In versions pioir to version 4.2.0 the Visual Logger Docker container was running under the ``root`` user. In version 4.2.0 it runs under user ``ogamma``. As a result, data files of the older version volume that had a root user as owner, not accessible in the new version.

To fix this permission issue, start the container once using configuration file ``docker-compose-migrate-to-4.2.0.yml``, running this command: 

```
docker compose -f docker-compose-migrate-to-4.2.0.yml up
```

It should print in the console output this message: `` Ownership of the folder /home/ogamma/logger changed to ogamma``

# ogamma Visual Logger as Kafka Source Connector

Now the OVL is also available as Apache Kafka Source Connector jar file!
Follow sections below to deploy it using docker Compose files from this repository on Confluent or Redpanda platforms.

## Running Visual Logger as Kafka Connector in Confluent platform

For details, please refer this quick guide: [Running Confluent service in Docker](docker/confluent/confluent.md)

## Running Visual Logger as Kafka Connector in Redpanda

For details, please refer this quick guide: [Setting up Redpanda broker and OPC UA Source Connector](docker/redpanda/redpanda.md)

# Running Visual Logger in Docker container hosted in Oracle Linux

For details please refer [this page](running-on-oracle-linux.md).