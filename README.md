# OPC-UA-Data-Logger
Integration tool, which performs 2 tasks:
1. Collects data from OPC UA Servers and stores it in PostgreSQL database (which might have TimescaleDB extension installed).
2. Acts as a back-end for Grafana SimpleJson data source plugin.

# Context Diagram
![OPC UA Data Logger - Context Diagram](https://raw.githubusercontent.com/onewayautomation/OPC-UA-Data-Logger/master/ContextDiagram.png)

# Getting Started with Docker image.

Easiest way to start using the OPC UA Data Logger is to pull Docker image: https://cloud.docker.com/u/onewayautomation/repository/docker/onewayautomation/opcuadatalogger. Please note that this image has only OPC UA Data Logger, so for complete setup it is not enough.

File ``docker/docker-compose.yml`` allows to pull OPC UA Data Logger image and additionally all required dependency images:
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
* Web GUI for OPC UA Data Logger will be available at http://localhost:4880;
* Database TimescaleDB - at localhost:4832. (Default user credentials can be found in docker-compose.yml file).
* PgAdmin - at http://localhost:4888; 
* Grafana - at https://localhost:4830

# Gettings started with Windows distribution package.

## Prerequisites

* Windows PC. 
  If you would like to try it on other OS, please contact me at the address ravil at onewayautomation.com, or create feature request issue here in GitHub. 

* Install Visual C++ 2017 redistributables (64 bit version):
  Latest downloads are available at https://support.microsoft.com/en-ca/help/2977003/the-latest-supported-visual-c-downloads
  
  Direct link: https://aka.ms/vs/15/release/vc_redist.x64.exe

	This file (vc-redist.x64.exe) is also included into the distribution package.

* Install / Configure PostgreSQL database.

  * If you have Docker, then you can use Docker compose file ``docker\timescaledb\docker-compose.yaml`` to start container with TimescaleDB (PostgreSQL extended to support time-series). Just navigate to this folder, and run ``docker-compose up``. Default values of user name, password and port number of the PostgreSQL server match with settings in the OPC UA Data Logger configuration file (by default ``config.json``). Change them according to your requirements.

  * Install PostgreSQL manually.
    * Download installer from page: https://www.postgresql.org/download/windows/ Versions 10 and 11 were tested and should work.
    * Create a user which will be used to access the database from OPC UA Data Logger. Default user name/password in the OPC UA Data Logger's configuration file are **uarest**/**uarest**.
    * Create database (default name is **test**); and assign user **uarest** as its owner. When OPC UA Data Logger starts first time, it will create required tables in this database. 
  
	Note that user credentials and database connection parameters can be changed later in the **config.json** file. 
 

## Installation and initial configuration.

* Download zip file from https://onewayautomation.com/opcua-binaries/opcua-logger-0.3.0.zip and unzip.
* If required, modify settings in the **config.json** file: http port number (default number is 8989), and settings to connect to the PostgreSQL database. 

## Running of the OPC UA Data Logger.

Open Windows comman line console, navigate to the folder where OPC UA Data Logger files are unzipped, and start application **OpcUaLogger.exe**. 
At the very first start, it will create tables in the PostgreSQL database. Before connecting to the frist OPC UA server (after adding it from GUI and attempt to browse), it will also generate OPC UA Application Instance Certificate, which might take some time.

The application has built-in web server to support web based GUI to configure it, so it will listen to http port. Windows operating system will pop-up dialog window to asking for permission to listen on the port, you will need allow it.

## Configuration of connections to OPC UA Servers and selection of OPC UA variables to monitor (log into the database).

Open web browser, and navigate to address http://localhost:8989

In the left side panel, click on **Add** button and add new connection. Note that currently web page needs to be refreshed in order to refresh the **Address Space** tree after adding/editing/deleting of an entry for OPC UA Server connection.

Browse OPC UA Server's address space and select one or more OPC UA Variable nodes which has numeric data type 
(those, for which value can be converted into **float** data type, for example, Byte, Int16, Int32, float, double. Complex type values can be logged too, but they are not decoded, instead length of their body in bytes is used as a value.).

Once one or more OPC UA Variables are selected, the button **Log** will be enabled. 
If you click on it, selected nodes will be used to create 
new records in the right side grid table. If a record has field **Active** checked and the field **Log to TSDB** is checked, then its value will be monitored by OPC UA Data Logger, and written (logged) into the PostgreSQL database. 
If a record has option **Read history from OPC UA Server** set to true, then OPC UA Data Logger will read historical values from OPC UA Server, when historical data is requested via simplejson data source's REST API for those variables. 

The following below screenshot illustrates typical GUI:
![Configuration GUI Screenshot](https://raw.githubusercontent.com/onewayautomation/OPC-UA-Data-Logger/master/Config-Gui-Screenshot.png)

## Configuring Grafana

You can skip this step if visualization using Grafana is not required.

* Install **Grafana** from https://grafana.com/
  * Instructions on Grafana web page suggest to use **wget** tool to download the installer. 
  If you don't have wget tool installed, then you can download it from here: https://eternallybored.org/misc/wget/
* Install **SimpleJson** data source plugin (instructions are available at https://grafana.com/plugins/grafana-simple-json-datasource/installation)
* Add data source of **SimpleJson** type, and configure it to connect to the OPC UA Data Logger endpoint (http://localhost:3000/grafana)
* Add new dashboard.
* Add panels to the created dashboard, and configure to get timeseries data from added SimpleJson data source.

![Grafana Screenshot](https://raw.githubusercontent.com/onewayautomation/OPC-UA-Data-Logger/master/Grafana-Screenshot.png)

### Using PostgreSQL data source.
It is possible also to get logged data values from PostgreSQL database directly, 
using PostgreSQL data source plugin for Grafana (installation is not required, included into Grafana by default).
Example of the SQL quesry can be found below:

>` SELECT
  $__time(time),
  value
FROM
  values
WHERE
  $__timeFilter(time) and sourceid='1'
`

Here **time**, **value** and **sourceid** are column names in the **values** table. 
You can figure out corresponding to the OPC UA variable **sourceid** from 
Logged Variables data grid on the configuration GUI.

Introduction video with more detailed instructions is available on youtube at https://youtu.be/yZdsyVz7hw0.