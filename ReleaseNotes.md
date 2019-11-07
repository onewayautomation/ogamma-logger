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
