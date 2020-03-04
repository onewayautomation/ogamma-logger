Version 0.8.4 2020-Mar-03
-------------------------

* Fixed issue: when there are multiple OPC UA Server connections configured in the address space, and there are multiple variable groups  with variables, and all of them are collapsed, and when group selection is changed, this causes infinite calls from browser to the backend. Can also cause application crash.
* Fixed issue: upgrade from older versions (prior 0.8.1) (Ubuntu and Docker versions) with configuration database of SQLite type does not completely upgrade tables, and does not report error.
* Upgraded some dependencies (web framework and ODB library) to newer versions.
* Docker image changed to stop container when application process stops.
* To support upgrades from older versions, when InfluxdB settings are loaded from ./data/config.json file, its mapping settings configured to be the same as in older versions (i.e. ``measurement`` will be set to ``d`` and tag will be set to ``n=[variable id]``).


Version 0.8.3 2020-Feb-29
-------------------------


* Fixed issue: Application crashes at attempt to activate or re-activate license.
* Fixed issue: Instance configuration changes sometimes not saved or not applied without restart.
* To be consistent with older versions, for InfluxDb modified values set by button ``Reset to defaults`` to the same settings as in versions prior 0.8.1 (i.e. ``measurement`` will be set to ``d`` and tag will be set to ``n=[variable id]``).
* Improvements in logging messages formatting and runtime error handling.
* Ubuntu executable binary is built without debug info to reduce size.

Version 0.8.2 2020-Feb-26
-------------------------

* Web server port number and number of threads now can be changed at runtime via menu ``Settings/Instances``.
* Fixed issue: application crashes if configuration database type is changed at runtime.
* Fixed issue: If more than one Collector Configuration is used, then in Grafana SimpleJson tag selector all variables from all configurations are displayed, while only those which belong to the configuration assigned to the instance should be displayed.
* Modified column names in Logged Variables table to match with time-series database type.
* Fixed issue: Column ``Status`` in ``Logged Variables`` table is writable, should be read only.
* Added text field displaying current instance name and ID.
* Fixed issue: in the Instances table link to open the instance page was not correct.

Version 0.8.1 2020-Feb 23
-------------------------

* Introduced limitations for Community Edition, which come into effect after 1 month since license activation, but not earlier than May 1, 2020. Refer to the User Manual for details.
* All configuration settings now can be modified via web GUI. Most changes are applied at runtime, without restart of the application.
* Added concept of Instances. Multiple instances of the application, running in the same machine or on different machines in the same network, will be manageable from single page. In this release database has support for this, but implementation is not complete yet. Refer to User Manual for details.
* Some default values for configuration settings are changed. For example, now log file and PKI (certificates) locations are changed:  their new location is in sub-folder of ./data folder, with unique name, which allows to run multiple parallel instances with the same work folder.
* For easier management of variables, added concept of grouping using Variable Groups. Variable Groups have global scope and available from all instances and OPC UA Server connections. They define default data collection parameters such as sampling and publishing interval. When variables are added from OPC UA address space, currently active group's settings are assigned to them.
* Added support to select multiple nodes from the address space and add them to the Logged Variables table.
* Added support for sorting by different columns in the Logged Variables table.
* InfluxDB measurements and tags now configurable via web GUI (columns Topic Name and Key Name). Default values can be generated automatically in different configurable ways.
* Log level changes applied at runtime without restart.
* Added feature to display real time value/status/timestamp for OPC UA variables in the Logged Variables table.
* Fixed few runtime crash issues.
* Added support for browsing of OPC UA Servers address space in cases when server does not return all references in one call, now consequitive BrowseNext requests are made and all references can be retrieved.
* Added support to store non-numeric data type values as strings in InfluxDB and Apache Kafka.
* Implemented support for microsecond resolution for InfluxDB.
* JavaScript files minified.

Version 0.7.1 2020-Jan-16
-------------------------

* Fixed issue of building address space tree in GUI, occurring when the same node is referred from multiple parent nodes.

Version 0.7.0 2020-Jan-12
-------------------------

* Added support for licensing. Now application requires activation using license key, which can be obtained for Community Edition using One-Way Automation on-line store at https://onewayautomation.com/online-store. License can be activated via Web GUI (menu `Setup/License`).
* Improved error handling.
* Changes in configuration file, related to time-series database connections. now appied without re-start, at runtime.
* Fixed issue "Log files cannot be accessed via Web GUI on Windows".
* Fixed issue "Reading data from InluxDB to Grafana fails".
* In the Logged Variables grid added feature `Column Chooser` to show or hide columns.
* Added link to Release Notes into the `Help and Links` menu.
* Added link to open configuration settings into `Setup` menu (currently not enabled though).
* Improved handling of temporary disconnections from time-series databases: now failed write batch is kept in the in-memory queue and written when connection is restored, eliminating data lost. If time-series database is not available at start time, data also cached in memory buffer.


Version 0.6.1 2020-Jan-01
-------------------------
* Maintenance release. Fixed runtime error issue (occurring when some fields in the Logged Variables table are edited).

Version 0.6.0 2019-Dec-28
-------------------------

* Added support for Apache Kafka.   
  Tested with different Kafka clusters:
  * Cloud instances, managed by https://www.confluent.io/confluent-cloud and running at following providers:
    * Amazon Web Services;
    * Microsoft Azure;
    * Google Cloud Platform. 
  * Running locally in Docker container (image https://hub.docker.com/r/bitnami/kafka)
* Parsing of json configuration file modified: now single line and muti-line comments are allowed.
* Windows version is now built with newer version of Visual Studio (2019), therefore version 2019 of Visual C++ redistributables are required to be installed.
* Newer version of dependency libraries are used.
* Size of log files is reduceed from 16 Mb to 8 Mb, for faster downloading with Internet browser.

Version 0.5.2 2019-Nov-09
-------------------------

* Added support for UserName identity token type on connections to OPC UA Servers;
* Added support for OPC UA deadband, so now data changes can be reported only when change of the value is greater than defined by deadband settings. 
* Re-build with the latest version of the OPC UA SDK, so now it can connect to OPC UA Servers running within containers, when Visual Logger is running outside of container, using host machines' name in endpoint URL.

Version 0.5.1 2019-Nov-06
-------------------------

Fixed issue: was not connecting to InfluxDB in secured mode (https://github.com/onewayautomation/ogamma-logger/issues/6)

Version 0.5.0 2019-Nov-02
-------------------------

* Added support for InfluxDB database (versions 1.7 and 2.0, https://www.influxdata.com/) (GitHub issue https://github.com/onewayautomation/ogamma-logger/issues/5)
* Fixed bug: After restart, tries re-create TSDB database, but fails and exits, if OS language is not English (GitHub issue https://github.com/onewayautomation/ogamma-logger/issues/4)
* Web framework upgraded to the newest version;

Version 0.4.2, 25 Aug, 2019
---------------------------

* Re-built with newer versions of dependencies;
* Added distribution package for Debian Stretch;
* Updated User Manual (available at https://onewayautomation.com/visual-logger-docs/html/)
