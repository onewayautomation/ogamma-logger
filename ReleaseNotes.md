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
