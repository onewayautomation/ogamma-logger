# ogamma Visual Logger for OPC - Release Notes.

## Known issues.

1. When InfluxDB time-series data is used to store data, and value in the field ``Database specific settings/json``, property ``precision`` value is set to either ``us`` (for microsecond) or ``ns`` (for nanosecond), data is written, but cannot be read back. It seems that the issue is on the InfluxDb side: it works fine in the instance of InfluxDB hosted by InfluxData but does not work with Docker image version quay.io/influxdb/influxdb:2.0.0-beta.
2. When the ``Refresh Data`` field in the ``Logged Variables`` table is set to automatic refresh mode, it is not possible to edit records in that table. The workaround is to turn data refreshing off before editing records.
3. Table ``Logged Variables`` has too many columns and not all of them fit well into the screen, and horizontal scrolling is not available, which causes problems viewing/editing them. Workaround: Use the "Column Chooser`` button in the right top corner of the table and select columns that need to be visible or hidden (usually not all columns need to be visible).
4. When OPC UA Server connection settings or logged variables settings are changed, to apply them, connections to all OPC UA Servers are closed and re-opened, and subscriptions and monitored items are re-created. When an application instance has a large number of server connections and logged variables, this might be inconvenient.
5. When communication with the time-series database is slow or broken, and there are Grafana sessions querying data via ogamma Visual Logger for OPC REST endpoint, this can cause issues with configuration GUI responsiveness. As a workaround, a separate instance can be created to serve the REST endpoint or the number of threads in the same instance can be increased (option ``Web Server Settings / Number of threads`` in the ``Instance Settings`` dialog window).
6. Reading of historical data from an Apache Kafka-type database ( processing of Grafana requests) can be slow when within the requested time range there are large numbers of records for variables with the same topic and partition as topic and partition for the variable for which data is being requested. The reason for this is that although they might have different keys, it is not possible to filter records by a key value, they are filtered in Kafka broker only by topic name and partition. So records for multiple keys are read, and then from them, records with the desired key value are selected, which takes considerable time.
7. If the configuration database is not available at start-up, then the configuration GUI is not accessible. This issue exists in versions starting from 2.1.16.
8. When a server node is added/removed/modified in the ``Address Space`` panel it might become empty although there must be some server nodes. In such case, the web page needs to be refreshed to view all the servers. 
9. Grafana endpoint is not compatible with the newest version of Grafana anymore.

## Release History.

### Version 4.0.5 - 2024-Oct-07

Fixed memory leak issue (happening when data is logged to SQL database) introduced in version 4.0.4.

### Version 4.0.4 - 2024-Sep-10

* For SQL-family of time-series databases added more options in the JSON field:
          
  * ``maxStringSize``: Maximum length of string type values. Values stored as a string are truncated to this length if they are longer than this maximum limit. Default value is 65535.

  * ``storeAllTypesAsJson``: If set to ``true``, values of any type (including numeric values) are stored in the column named as the value of the option ``storeJsonValuesInColumn``. This can be used if the database supports JSON type columns, as ``json`` or ``jsonb`` types in PostgreSQL/TimescaleDB. Default value is ``false``.

  * ``storeJsonValuesInColumn``. This option si used when the option ``storeAllTypesAsJson`` is true. Values of any type (including numeric values) are stored in the column named as the value of this option. Default value is ``string_value``. Note that if the column name is different than default ``string_value``, it must be created by the user.

* Added new options in the ``OPC UA Server advanced options`` dialog, used when OPC UA server address space is being discovered:

  * Option ``maxBrowseRequests`` to limit number of parallel ``Browse`` or ``BrowseNext`` requests sent to the server. Default value is ``5``.
  * Option ``browseVariablesOnDiscovery``: when set to ``true``, variable nodes are included into the list of nodes passed to the browse selector script. If the node is selected to browse, it allows discovery of members of complex type variables. Default value is set to ``false``.

    Note that there is also another way to discover members of complex type variables: by setting value of the field ``BrowseMembers`` to ``True`` in the variable selector script.

* When connecting to OPC UA Servers, added a step to read the value of the node ``Objects / Server / Server Capabilities / Operation Limits / MaxNodesPerRead``. If this read value is greater than 0, then it is used if periodic reading of variable values is configured in OPC UA Server connection settings, and the value configured by the option ``MaxNodesPerReadRequest`` is 0 or greater than the value read from the server, to limit the number of nodes read in one Read service call.

* After connecting to the OPC UA Server, values of nodes ``Objects / Server / Server Capabilities / Operation Limits / MaxNodesPerRead`` and ``Objects / Server / Server Capabilities / Operation Limits / maxMonitoredItemsPerCall`` are read, and values are stored in the connection advanced options in fields ``operationLimit.maxNodesPerRead`` and ``operationLimit.maxMonitoredItemsPerCall`` respectively. They are not used in further connections, stored for information only.

* Modified behaviour of variable selector used to auto-discover variables: - now only nodes with ``NodeClass`` attribute equal to ``Object`` or ``Variable`` are browsed.

* Fixed issue: writing to the TSDB type of SQLite or MS SQL or PostgreSQL/TimescaleDB might fail if the option ``logClientTimetamp`` is turned on, and the value type is complex (structure) type.

* Fixed issue: OPC UA Server advanced configuration option ``maxMonitoredItemsPerSubscription`` is not applied. Additionally now after connection to the server, values of the node ``Objects / Server / Server Capabilities / Operation Limits / MaxMonitoredItemsPerCallPerRead`` is read, and critical message is logged in the SDK log file if value of this option conflicts with the value read from the server.

* Fixed issue: Complex type values cannot be decoded if they have child members of complex type that in turn have members with data type of arrays of basic type values.

* Updated company logo image.

### Version 4.0.3 - 2024-May-04

* Fixed issue: placeholder ``[BrowsePath]`` used in the field ``VariableTag`` of the Logged Variables table is not replaced by the actual value, causing incorrect MQTT topic composition.
* Default value for the environment variable ``OVL_AUTH_TYPE`` changed to ``JWT_BUILTIN``, to allow authentication via proxy when this variable is not defined.

### Version 4.0.2 - 2024-Apr-19

* Fixed issue: ``variable selector`` fails when used against some OPC UA Servers.

### Version 4.0.1 - 2024-Apr-16

* Fixed issue: application crashes if configured to authenticate users using JWT token and the user has no email defined.
* Fixed issue: the ``variable selector`` feature might not work when the application runs as a Docker conrtainer.

### Version 4.0.0 - 2024-Jan-10

* Added support to authenticate and authorize the user of the configuration GUI web interface by external Identity Provider. Currently, it is applicable only when the application is accessed via reverse proxy. Tested in setup with nginx, oauth2 proxy, and keycloak.
* Fixed issue - configuration GUI does not work when accessed via reverse proxy.
* Fixed issue - range of time period stored in the local storage sometimes is not displayed correctly in the ``Statistics``  dialog window.
* Fixed issue - deleting of records in the local storage might fail if the size of the local storage database is close to the maximum. The issue was caused that to delete forwarded records the local storage needs to have some free space. Fixed by automatical expanding of the database.
* Fixed issue - retention duration of the InfluxDB database is not detected correctly in case if non-default retention policy is configured for the database.
* For InfluxDB, added options:

  - ``retention duration `` - retention duration in the format of ``1w2d3h4m5s``, where numbers before ``w``, ``d``, ``h``, ``m``, ``s`` mean respectively weeks, days, hours, minutes, and seconds. The default value is an empty value. If this option is empty, then the retention period is read from the InfluxDB database. 
  - ``actionForOutOfRangeTimestamps`` - defines what to do if a value with a timestamp older than retention duration is being written. Possible values are:

    - ``forward`` - timestamp will be corrected to the earliest possible value plus some delta, defined by another option ``retentionDelta``.
    - ``skip`` - those values will be skipped (not written to the database).
  - ``retentionDelta`` - spare time defined in the same format as ``retentionDuration``. Added to the earliest possible timestamp (defined by subtracting ``retention Duration`` from current time), when the option ``actionForOutOfRangeTimestamps`` is set to ``forward`` and the out-of-range timestamp is corrected.

* For SQLite type database, the default value for option ``insertSqlCommand`` is changed to ``INSERT OR REPLACE``, to avoid duplicate records issues.
* Fixed issue: initialization of MySQL database fails preventing logging to it.
* Added feature to create HTTPS certificate file if it does not exist. Additionally, also certificate sign request is created and saved in a file. It can be used to sign the certificate by third-party certificate authority.
* Implemented feature to limit the number of returned browse results by the maximum number defined by option ``browseTotalReferences``. Also, the total duration of time to browse is limited by the option ``browseTotalDuration``.  The purpose is to keep the GUI responsive in cases when the OPC UA Server has a large number of nodes under one parent node. If not all nodes are returned due to these limits, a notification message is displayed. To add all variables in such cases, the auto-discovery feature can be used.

### Version 3.0.2 - 2023-Nov-27

* Data type of columns ``Sampling interval`` and ``Publishing interval`` in ``Logged Variables`` and ``Variable Groups`` tables is changed from integer to floating point, to allow collecting data with rates faster than 1 millisecond.

* The default value for column ``Sampling Interval`` in the ``Logged Variables`` and ``Variable Groups`` tables is changed from 1000 to -1, which means to sample with the same rate as the publishing interval.

* Added columns ``Revised sampling interval`` and ``Revised queue size`` in the ``Logged Variables`` table, so it is easy to check from the GUI what values are actually used (revised and accepted) by the server.

* Modified database initialization SQL scripts for MS SQL and PostgreSQL to create the index on fields ``sourceid`` and ``time`` for the values table only when the table is created initially. This allows deletion of the index when it is not required, to improve ingress performance.

* Modified data type of the advanced option ``readValuesInterval`` in OPC UA Server node settings from integer to floating point, to allow periodic reading of variable values with sub-second intervals.

* Added logging of records returned in FindServers and GetEndpoints responses to help troubleshoot connectivity issues.

* Fixed issue on composing of topic name from a template having the ``[BrowsePath]`` placeholder.

* License terms changed, added section 2.6:

  2.6. CUSTOMER should not abuse free-of-charge Community Edition licenses. It is allowed to run only one instance of the application with a Community Edition license at a time per CUSTOMER unless there is written permission obtained from the VENDOR.

* Improved license reactivation workflow: now no restart is required to apply new limits on a number of variables, servers, and groups after re-activation.

* Updated dependency libraries (OPC UA SDK, boost, paho-mqtt, OpenSSL).

* In the Time-series database connection settings dialog window, for MQTT type connections in JSON settings:

  * added ``maxBufferedMessages`` (default value 1000), ``maxInflightMessages`` (default value 100) and ``numberOfConnections`` (default value 1), to fine-tune performance.

  * changed the default value for option ``publishQos`` from 1 to 0, to provide higher publishing rates.

  * Fixed issue with the message buffer size reaching max limit.

* Fixed issue: The ``Browse Path`` column in the ``Logged Variables`` table sometimes might be not correct (starts with the word ``undefined``).


### Version 3.0.1 - 2023-Sep-10

* Fixed issue: part of topic and payload templates following after placeholder [BrowsePath] can be truncated.

### Version 3.0.0 - 2023-Aug-27

* Added new ``Auto-Discovery`` feature to recursively browse OPC UA Server's address space and select variables using criteria defined in Python scripts. The feature can be accessed using new dialog window ``Browse and select variables to log`` opened via context menu in the ``Address Space`` panel. This feature allows not only adding new variables to log, also can be used to mass edit or delete existing variable records too.

* Improved displaying variable nodes in the ``Address Space`` panel: now they have different color icons:
  * variables which are already in the ``Logged Variables`` table has icon depending on the value in the column ``Log to TSDB``:
    * ``Log to TSDB`` is ``true`` (that is, values are logged to the database) - turquise icon.
    * ``Log to TSDB`` is ``false`` (variables are not active, not logged to the database) - blue icon.
  * variables which are not in the Logged Variables table: orange icon.
* Implemented requirement to allow downloading of application certificate and its issuer certificate with CRL only for authenticated users.
* Added 2 more columns in the Logged Variables tables - ``Browse Path`` and ``Browse Name``. Their values for existing records can be updated using ``Auto-Discovery`` feature.
* Added support to use OPC UA variable's ``Browse Path`` to map to the TSDB schema, For example, MQTT topic can be composed automatically using Browse Path.
* Added hint help text to display when the ``Address Space`` panel or ``Logged Variables`` table has no data to display.
* Fixed issue: when multiple OPC UA variables have a reference to the same HA Configuration object by reference of HasHistoricalConfiguration type, and when these variables are expanded, only first variable can be expanded, others cause JavaScript error (duplicate key at attempt to add the node to the Address Space tree). Now references of the HasHistoricalConfiguration type excluded from browse results and not displayed in the Address Space tree. If such object's child variables need to be logged, they can be added manually.
* Adjusted default size of some dialog windows.
* User Manual is updated accordingly.

### Version 2.2.2 - 2023-Mar-12

* For SQL family time-series databases added option ``logClientTimetamp``. When it is set to ``true``, client side timestamps (assigned when data value has been received from OPC UA Server) written to the database, in new column ``client_time``. This can be helpful in case if the server might have incorrect system time.
* Implemented persistence of dialog windows sizes between sessions.
* Fixed issue: configured "precision" option is not used in SQLite timestamp values (always was logged with millisconds precision). 
* Fixed issue: disabled OPC UA server's variables are counted as active when number of variables is limited, which causes not logging of active variables from active servers, even though their number is within limits set by the license.
* Improved license upgrade workflow (de-activation and re-activation of the license): now for 1 hour after de-activation the application functions as normal, and after re-activaiton changes can be applied without restart.
* Improved uploading of the AMU license file - now after upload completion the status text is updated before re-opening of the license status dialog window.

### Version 2.2.1 - 2023-Feb-26
* Revised selecting variable nodes from the address space panel and adding them into the Logged Variables table when the server has large number of variables under single node (more than one thousand). If number of variables is too large (greater than 5000), it is recommended to consider adding that large number of variables either by direct access to the configuration database or using Python scripts, as it is described in the User Manual. In case of anyway using the GUI, then please note that updating of the Address Space panel can take considerable time (up to several minutes). It is recommended to select and add no more than 2000 nodes at a time, otherwise "unspecified network error" might occur. Note that before auto-selecting of range of nodes (by first selecting start node, and then keeping Shift key pressed when the end node is selected), the Refresh Data should be turned Off. Please also note that when the range of auto-selected nodes has thousands of nodes, it can take minutes to complete selection of all nodes.
* Fixed issue introduced in version 2.2.0: variable groups cannot be created with error "Maximum number of variable groups[0] allowed by license terms reached".
* Fixed issue: application crashes if OPC UA Server has a certificate with validity start date earlier than year 1950.
* Newer versions of some dependency libraries used.

### Version 2.2.0 - 2023-Feb-07

* Important: Added feature to enforce the requirement to have valid annual maintenance and upgrades license to run application executable builds starting from version 2.2.0. Before upgrading to new versions please check if it can run with your licenses. For details please refer to the online User Manual.
* Fixed issue: browsing of an OPC UA node that has references of different types to the same node (for example, references of types Organizes and HasNotifier), causes duplicate nodes in the Address Space.
* Fixed issue: browsing of nodes with node id of string type containing special characters can fail.
* Improved viewing of the configuration GUI in displays with higher resolution.

### Version 2.1.18 - 2022-Dec-14

* Fixed issue: Application craches if time-series database type is InfluxDB 1.x and variable value of string data type has invalid UTF-8 value.
* Fixed issue: Fields in the ``Collected values`` group in the statistics window do not include values received by periodic calling of Read requests (this is the case when option ``readValuesInterval`` is UA Server conneciton settings has value greater than 0.
* Fixed issue: Writing to SQL family databases string type values containing single quote symbol ``'`` or invalid UTF-8 strings causes failure of the write transaction and forwarding data values is interrupted. Now invalid characters are replaced by symbol ``�``.

### Version 2.1.17 - 2022-Nov-14

* In JSON configuration settings for the SQL family of time-series databases added 2 new options, with the goal to provide access to the values of columns ``Display Name`` and ``OPC UA Node Id`` from the ``Logged Variables`` table when running queries in the time-series database. 

* ``writeDisplayName``: If set to ``true``, value of the column ``Display Name`` from "Logged Variables" table for the variable will be written to the time-series database together with timestamp, status and data value, into column ``display_name``. Note that this column is not created automatically, it should be created by the user in the table ``values``.

* ``copyVariablesTable``: If set to ``true``, then in the database new table ``variables`` is created, with columns ``id``, ``display_name`` and ``node_id``. When the Collector Agent starts, records in it synchronized with records from the ``Logged Variables`` table. This allows to access display name and OPC UA Node id from the same database where time-series data is stored.

* In JSON configuration settings for the SQL family of time-series databases added option ``tableName``, which allows to store data values in the time-series database in a table with custom name instead of default name ``values``.

* Fixed issue: Browsing of the OPC UA Server node from the Address Space panel of the GUI fails if OPC UA node identifier is type of string and contains either " or " or " and " in it.

### Version 2.1.16 - 2022-Oct-16

* Fixed issue: If configuration database of PostgreSQL type is not available at application start time, data flow might be interrupted even after the database becomes available.

### Version 2.1.15 - 2022-Aug-21

* This build is released only for RedHat Enterprise 8.6.
* The dependency library used to communicate with Apache Kafka has been updated to newer version.

### Version 2.1.14 - 2022-Aug-14

* To increase throughput of writing, for SQL databases (exceptiong SQLite) added JSON option ``numberOfConnections``. This number of connections to the database is created in parallel, each in its own thread. This allows to write data to SQL databases with rate 100,000 values per second and higher, depending on the database performance and connection bandwidth.
* In the Instance configuration settings, added option ``OPC UA SDK Settings / Number of timer threads``. It might require adjustment in high load cases.
* In Windows and Ubuntu distributions added folder ``CreateConfigDb`` with Python script to create new Collector Configuration with large number of servers and variables, to use in pertormance tests. It is added to the ogamma-logger repository at GitHub too. This folder has also Powershell script to start multiple instances of the OPC UA Demo server to use in tests. 
* Added command line option ``--rescueMode``. Contact support for more details about using of this option.
* Added option ``scanAtStart`` in the instance's local storage settings. When this options is turned on, ogamma Visual Logger for OPC at start-up scans all records stored the local storage, instead of using value stored in the database statistics area. 
* Fixed issue: when collector configuration is deleted, servers and logged variables are not deleted from configuration database tables.
* Fixed issue: OPC UA Server connection advanced option ``methods`` is ignored if both options ``readTypeDefinitionsOnConnect`` and ``readXmlTypeDictionaryOnConnect`` are disabled.
* Updated User Manual: added How To section ``How to add OPC UA Server connection settings and logged variables using Python scripts``.

### Version 2.1.13 - 2022-Jul-17

* In the ``Logged Variables`` table added column ``Expanded value`` to display values for variables of complex data type. By default this column is not visible. 
* In MQTT database JSON settings added options ``usePayloadTemplate`` and ``payloadTemplate`` used to define custom payload format. Default values are ``false`` and empty string.
* Fixed issue: complex type definitions are not read from an OPC UA Server although advanced options ``readTypeDefinitionsOnConnect`` and ``readXmlTypeDictionaryOnConnect`` are set to ``true``. Now these options by default set to ``false``. Note that for existing server connection settings toggling them off on an can be required to enable support of complex data types.
* Fixed issue: after changing of the value of the column ``Store Mode`` in the ``Logged Variables`` table it is not displayed correctly (shows previous value), even though in the backend database the value actually is changed.
* License terms clarified.
* User Manual is updated.

### Version 2.1.12 - 2022-Jul-06

* Fixed issue: cannot connect to the OPC UA Server in secured mode when the server certificate's public key length is 4096. Particlularly, this issue was preventing secure connections to the TwinCAT OPC UA Server.
* Added feature to define using environment variables default user id and password to login to the configuration GUI web page after initialization of the new configuration database. After login, the default password must be changed to new password.

### Version 2.1.11 - 2022-Jun-27

* Fixed issue: dialog window Tools/Statistics displays an incorrect range of time period and a number of records in local storage.

### Version 2.1.10 - 2022-Jun-26

* Fixed issue: Connection error is reported as "Unexpected CreateSession response is received" when server side returns message of ``OPC UA ERR`` type to Open Secure Channel request (typical use case - when the application instance certificate is not accepted by the server).
* Modified logic of composing MQTT payload - now it is possible to use custom text format template (such as JSON or CSV) for the payload, similar to the implementation in Confluent and Kafka.
* Added few options to fine-tune TCP binary message sequence header border values (starting values and values used after wrap-around), to facilitate better interoperability with servers built according to different verions of specifications: ``newChannelStartingSequenceNumber``, ``maxUseableSequenceNumber``, ``startingSequenceNumberAfterMaxUsed``, ``newChannelRequestId``. In most cases default values will work.
* Modified the way how timestamps for periodically read values is verified and adjusted. Now not only source timestamp, but also server timestamp is read. If the source timestamp is older than defined by the ``readValueMaxEdge`` option, then rhe server timestamp is used in logged records. Before, response or request header timestamp was used, which was causing inconsistent results when server system time is out of sync.
* Added new advanced option for OPC UA Server configuration settings: ``maxSentChainLength``, which defines maximum number of certificates in a chain (including CA certificates) sent to the server in OpenSecureChannel and CreateSession requests. Default value 0 (unlimited), which results behaviour consistent with the previous versions.
* Confluent and Kafka: fixed issue: when interrupted connection with the Confluent/Kafka database is restored, data logging does not resume, with error message in the application log f ile "the internal queue is full, waiting...".
* Grafana SimpleJson endpoint: reading data from Confluent/Kafka is opmitized.

### Version 2.1.9 - 2022-May-22

* Modified value reported for the standard server variable ``Objects/ServerStatus/State`` when disconnection is detected: now it is set to value 7, which means communication error. Before the value was always 0 (Running). This modification allows easier detection of disconnections from OPC UA Servers and representing connection state in dashboards.

* Modified grafana endpoint: if there are no values for the queried time range, then last value is added to the result set with adjusted tiemstamp, if the time range is later than existing last value's timestamp. This allows to display last value in dashboards when variable value is not changing.

* Fixed issue: Docker container running the application logs segmentation fault error and hangs when communication with OPC UA Server is interrupted and reconnection fails.

* Fixed issue: Reconnection with OPC UA Server fails with error BadSecureChannelIdInvalid.

* User Manual's How To section updated with example on interacting with the ogamma Visual Logger for OPC over REST API from Python code. 

### Version 2.1.8 - 2022-Mar-23

* Implemented fix for the issue: Writing values to the Kafka database fails when OPC UA Server reports data values with timestamps earlier than 1/1/1970. The most common use case is when the timestamp is empty. Added option ``allowNegativeUnixEpochTime``. When this option is ``false``, then negative Unix timestamp values will be reset to 0. The default value is ``false``.

* Fixed issue: the placeholder [ClientTimestamp] is not set to the correct value in the payload in Kafka/Confluent database when values are read periodically by calling Read service.

### Version 2.1.7 - 2022-Jan-21

* Changes applicable when data values are logged to Apache Kafka or Confluent type database:
	
	* Added feature to log client side timestamps in JSON format payload, using new placeholder ``[ClientTimestamp]``.
	*	Added option ``timestampFormat`` to configure format for timestamps: 
		* ``default``: (existing implementation, UTC formatted string with space symbol used as delimiter between date and time;
		* ``ISO 8601``: ISO-8601 compliant string, that is using syumbol 'T' as delimiter between data and time, and additional symbol 'Z' at the end to indicate UTC timezone.
		* ``OPC UA``: 64-bit integer with the value same as defined by OPC UA Specification (number of 100 nanoseconds since 1 Jan, 1601).
		* ``Unix``: Unix format time, number of seconds (if option ``precision`` is set to ``s``), or milliseconds (when option ``precision`` is set to value other than ``s`) elapsed since 1 Jan 1970.
		
* Fixed issue: changes in OPC UA Server configuration settings used in topic/key values require application restart to be applied.
* Modified sql script file used to initialize time-series database of PostgreSQL type (removed attributes causing preventing using compression).
* For SQL family of time-series databases the option ``initScriptName`` made visible in configuration dialog window, to allow using of alternative database initialization script file.
* For PostgreSQL type database modified default value of the option ``insertPostFix`` to ``ON CONFLICT (sourceid,time) DO NOTHING`` (this option is used to eliminate duplicate record errors).
* For SQL family of time-series databases added option ``writeVariableDataType`` with default value ``true``. It is used to alter what data type code is written into the ``data_type`` column: when true,  

### Version 2.1.6 for Raspberry Pi - 2021-Nov-17

* Created experimental build of the Docker image for Raspberry Pi, based on 32 bit debian/bullseye. The image is available at https://hub.docker.com/r/ogamma/logger-pi32

### Version 2.1.6 2021-Nov-03

* Improved performance storing data values to Confluent and Apache Kafka databases, by adding support for parallel producers and deleting records from the Local Storage in batches.
* Fixed errors happening when Collector Agent is disabled.
* Fixed issue with some records staying in the Local Storage when connection with Kafka is interrupted (increased flush timeout, also made it configurable: added option "flushTimeout" for Producer).
* Fixed issue: CPU spins when connection with the database cannot be established.
* Fixed issue: collection statistics reset when Collector Agent is disabled.
* Fixed some runtime errors happening when Collector Agent was disabled / enabled multiple times.
* Some dependencies updated to newer versions.

### Version 2.1.5 2021-Oct-19

* Added feature to periodically read and log variable values with time interval specificed in server configuration settings, even when they do not change. This is useful when logged values are displayed in graphs, like in Grafana, to provide that at least one value exists within display time window, instead of reporting that no value found.

* When InfluxDB is used as a time-series database, now it is possible peridically write application status to the database, with configurable interval, measurement and tags.

### Version 2.1.4 2021-Sep-27

* Fixed connectivity issue: does not connect to OPC UA Servers in secured mode if advanced certificate validation option ``acceptAnyCertificate`` is ``false``.

### Version 2.1.3 2021-Sep-19

* Rebuilt with newer version of the OPC UA C++ SDK, with fix for connectivity issue happening when endpoint URL is longer than 96 symbols.

### Version 2.1.2 2021-Sep-05

* For the SQL family of databases, modified schema of the database table ``values`` where time-series data is stored. Specifically, added column ``data_type`` to store data type code, and columns ``int_value`` and ``string_value``, to store values of different data types, including arrays and complex type values. It is recommended to review configuration options for SQL databases, and set value for the option ``valueType`` to  ``default``, which facilitates storing values with the most accuracy.

* Minor improvement of the GUI: now after adding child nodes of a node from Address Space tree view, ``Logged Variables`` table is updated automatically.

### Version 2.1.1 2021-Jul-10

* For Confluent and Apache Kafka databases added JSON option ``decimalFormatSpecifier``, to format double and float type values written into the database. Default value "" preserves existing behaviour. Formatting syntax is described here: https://fmt.dev/latest/syntax.html

* Re-built with the updated version of the OPC UA SDK, with fixes for connectivity issues.

* Added feature to change icons for server nodes in the ``Address Space`` panel depending on the current state of the server connection.

* Fixed issue occurring in Windows machines with non-English language pack: Connection with OPC UA Servers cannot be established and application crashes when dialog window Tools/Statistics is opened.

* For Confluent and Apache Kafka databases fixed the issue: large integer numbers written with lost accuracy (values are rounded, not all digits are written).

* Added feature to support writing of values in hexadecimal format to integer type variables. For example, value formatted as `0xFFFF` can be written to a variable of UInt16 type.

* Docker container image base OS changed from Ubuntu 18.04 to Ubuntu 20.04. As a result the image has no vulnerabilities with severity level higher than low level.

* Fixed issue: when the application is running in Ubuntu 20.04, connection to MS SQL database cannot be established with error that driver file cannot be found.

### Version 2.1.0 2021-Jun-25

* Added new feature: client-side deadband support. That is: if the OPC UA Server does not support absolute or percent deadband, then ogamma Visual Logger for OPC can filter data changes on its own, logging only those data changes which differ from previously logged values by configured deadband value. The feature can be enabled at the server connection level, by setting options ``supportsAbsoluteDeadband`` and ``supportsPercentDeadband`` in the ``OPC UA Server Advanced Options`` dialog window to ``false``.

* Added new feature: support for complex data types. This allows to log values for variables that has complex data type, like the ``ServerStatus`` node. It is implemented not for all databases yet, only for InluxDB, Confluent and Apache Kafka. Complex type data values can be logged in 3 different modes: 
  * Encoded - whole data value is stored in original OPC UA binary encoded format, converted into Base64 string.
  * Expanded Members - data fields are expanded up to primitive type values, and each leaf field value is logged individually. Also it is possible to configure for each field deadband settings, and turn on and off logging for that field (only for InfluxDB).
  * JSON String - data value is expanded into pritimite type fields, and stored as JSON string.
  
  Note: Unions are not supported yet.
 
* Added new feature for Confluent and Apache Kafka: now payload can be formatted using payload template.

* Fixed issue: when datachange filter with deadband is set, filter trigger is set to STATUS_0 instead of STATUS_VALUE_1, resulting to not getting data changes when variable value is changed in the server.

* In InfluxDB database connection settings, field key name for data values (JSON option ``fieldKeyNumericValue``) now can contain one or more placeholders. For example, instead of default field key ``v``, you can use ``[ServerTag]-[VariableDisplayName]``.

* For InfluxDB database logging of OPC UA Status values now can be skipped, if the field key for it is set to empty string.

* Added support to log variables with node id identifiers of GUID and Opaque type.

* Added feature to log arrays (InfluxDB only).

* JavaScript code used to display the Main menu is now stored in separate file ``mainMenu.js``, in original format (not minimized), to allow its customization (so un-used links can be removed, or new links can be added).

* In the configuration GUI the build number is also displayed additionally to the version number.

* Minor changes in the GUI look and feel (layout aligments, added tooltips, etc.)

* Fixed issue: application crashes if port number for the instance is modified via GUI.

* Fixed issue: real time data status is displayed as Good although the UA Server is not available;

* Fixed issue: Log files cannot be viewed via GUI in Windows installations.

* Fixed issue: In the time-series database configuration settings dialog window, when the value of the field Type is changed, it is not applied. 

* For InfluxDB database new JSON option added: ``ignoreWriteError``. It allows to ignore errors occurred when data is written to the database and continue writing next data values. This is intented to be used when some invalid data value was received from the server, and failure on writing it blocks writing of next values. Without this option attempts to write this value would be repeated infinitely. It is expected that normally it will be set to ``false``, and set to ``true`` for short period of time, just to skip this data value causing an error.

* New option is added in the time-series database configuration settings: ``replaceEmptyValueWithLastValue``. If it is set to "true", then in cases when empty value with bad status is received from the server, the previous value will be stored, so in graphs there will be no spikes to 0.'. Default value is ``false``.

* Fixed issue: time range of stored data values and duration sometimes displayed not correctly in dialog window Tools/Statistics.

* For the variable ServerStatus/State, when data change with bad status is received from the OPC UA SDK layer (which usually happens at disconnection due to communication error), empty value is replaced with value 7 (Unknown enum value). This allows connection status to be monitored and recorded into the database.

* Updated User Manual to reflect changes. Also, added new section on installing of the ogamma Visual Logger for OPC as Microsoft Azure IoT Edge module. And added few useful tips into the ``How To`` section.

* For PostgreSQL, new options are added to handle duplicate records issue. Refer to the new topic about this in the ``How to`` section of the User Manual.

* Improved reporting of the connection errors for PostgreSQL/TimescaleDB in the Tools/ Statistics dialog window.

* The underlying database engine used as a Local Storage changed and optimized. The number of configuration options for it minimized, the most important ones are folder name and database size. Database file with the configurable initial size is created to guarantee that it will be available to use. The Statistics dialog window is updated to display used database space, currently configured size, and available space in the disk. It is possible to configure the Local Storage to expand automatically when it becomes full.  Sife of expansion and maximim size are configurable too.

* In the ``Logged Variables`` table added page selector (at the top right corner), so it is possible to quickly move to the desired page. 

* Modified implementaiton of the context menu ``Log all first-level children`` in the Address Space panel - now preliminary browsing / expansion of the node is not required. This allows to add as many as 100,000 of nodes in a few seconds.

* Added more advanced configuration options for OPC UA Server node settings:
  
  * ``maxMonitoredItemsPerSubscription`` - this option allows to limit number of monitored items per subscription. This allows to solve issues caused by messages becoming too large, exceeding encoding limits supported by OPC UA Servers.
  * Limits for transport layer message sizes now can be increased to support large messages;

* For diagnostic/troubleshooting purposes new field is added in the ``Logged Variables`` table header (around central part), which displays active number of variables with bad status and with good status.

* Added new feature optionally call some methods on the server after connection. Particularly, this feature can be used to configure the server before subscribing to monitored items. One of the use cases is when Unified Automation OPC UA Demo server is used for tests, which have by default 1000 variables under ``Objects/Demo/007_Massfolder_Dynamic`` folder. Now it is possible to call its ``AddNodes`` method and increase number of nodes before subscribing to monitored items. For detais refer to the User Manual, How to section.

* Some docker files updated to use newer versions of images. InfluxDB 2 database now is not automatically initialized, needs to be initialized manually via GUI. Some mapped volumes are changed too.

* Fixed issue: in case when InfluxDB is used as a time-series database, and when the server reports data value with timestamp older than InfluxDB database/bucket retention policy, write operation fails. Now in those cases timestamp is corrected to be 10 seconds newer than the oldest possible timestamp. Those cases logged in the log file with level ``warning``.

* Fixed issue: in case when InfluxDB is selected as a database type in the time-series database settings dialog window, logic of the Test Connection button does not detect errors in organization name, bucket name or invalid token.

* Fixed issue: in InfluxDB 1.x, when the JSON option ``convertNumericValuesToDouble`` is set to ``false``,  unsigned integer numbers follow by symbol ``u``, which is not supported in this version and causes write failures (was added in 2.x).

* Some dependency libraries updated to newer versions. Particularly, newer version of the OPC UA SDK has fix for deadlock issues, happening when multple requests performed in parallel with large transport layer messages that are transferred in chunks. 

### Version 2.0.2 2021-Jan-26

* Fixed issue: downloading CA CRL fails (via menu ``Settings/Download Certificate/CA CRL``).
* Fixed issue: application might crash when writing to InfluxDB database repeatedly fails if JSON option ``numberOfConnections`` is greater than 1.

### Version 2.0.1 2021-Jan-18

* Fixed issue: cannot connect to the InfluxDB database in secured mode.
* Fixed issue: InfluxDB custom tag values (``Variable Tag`` column values defined in the ``Logged Variables`` table) are not applied if Tags Generation Mode is not set to ``Use JSON option "tagsTemplate"``.

### Version 2.0.0 2021-Jan-14

* Store and forward feature changed: now instead of in-memory buffer, file-system based local storage is used as a buffer. As a result, when connection with the target time-series database is lost, usage of RAM is not increased, data is stored in local buffer and therefroe data is not lost in case of restarts.
* Added support for certificate trust lists management (new menu command ``Settings / Certificates Management``. As a result, after upgrade to this version, connections to servers in secured mode would initialially fail. To allow connections, trust to the server certificate needs to be configured.
* Added feature to view server certificate if it is not trusted or cannot be validated, and add it to the trusted certificates list.
* Added feature to set precision of float data values stored in PostgreSQL and TimescaleDB databases (now can be stored as 64 or 32 bit float).
* Fixed issue: when the connection is restored after disconnection due to communication error, periodical secure channel renewal stops.
* Fixed issue with duplicate records when SQLite is used as a time-series database.
* Improved JSON editor used to edit other settings in TSDB condfiguration dialog.
* In the Server node settings dialog window added button ``Edit Advanced Options``, which opens separate dialog window to modify advanced confifuration settings, including certificate validation rules.
* For time-series databases for which topic name or measurement are applicable (InfluxDB, Confluent, Apache Kafka, MQTT), modified logic how JSON option topicName or meaasurement is applied: now they will be used only if the field ``Measurement Generation Mode`` is set to ``Use JSON option measurement`` (for InfluxDB), or field ``Topic Name Generation Mode`` is set to Use JSON option topicName (for others). It is recommended to revise time-series database settings before and after upgrade.
* Logged Variables table: modified scroll mode to support horizontal scrolling. Note: to enable it in upgraded versions, browser cache needs to be cleared.
* Logged Variables table: added column ``Variable Tag``, where variable-specific values can be entered, and then it can be referenced from ``tagsTemplate`` option by placeholder ``[VariableTag]`` to compose InfluxDB tags. The column ``Tags`` is not editable now, it will present composed values of the tags.
* Fixed issue: connection to the server fails in secured mode if number of monitored items is large.
* Dependency libraries updated to newer versions.
* In the OPC UA Server connection advanced settings added options ``dnsMap`` and ``urlMap``, which allow to connect to servers in cases when host or IP address they return in the endpoint is not accessible from the machine where ogamma Visual Logger for OPC is running.

### Version 1.2.5 2020-Nov-30

* Fixed connectivity issues:
  
  * incorrect Endpoint URL was used in TCP binary Hello and CreateSession messages, which was causing some servers to refuse the connection.
  * communication layer improved to handle tampered network packets.
  * automatic reconnection feature improved.

* Fixed bug: field clientDescription / productUri was not set in the Create Session request.
* User Manual is updated, and now, additionally to the online version, it is included in the distribution packages, for easy access from local networks without access to the Internet.
* For MQTT type database fixed runtime exception happening in the case when the configuration is modified during unstable connection with the broker.
* For InfluxDb, Kafka, Confluent, and MQTT type databases revised how mapping from OPC UA to measurement/topic name/tags/keys is implemented: added new selections ``Use JSON option ...`` and ``Use OPC UA Node Id``. It is recommended to check the current mapping implementation before upgrading to this version and create a full backup, and after the upgrade verify that mapping is correct. Refer to the User Manual for complete mapping details.
* For InfluxDb type database added JSON option ``allowSpaceInMeasurementAndTags`` which allows InfluxDB measurement and tags to have space symbol.
* For InfluxDB string type values added escaping of special symbols.
* InfluxDB field names for value, data type and status made configurable using new JSON options ``fieldKeyNumericValue``, ``fieldKeyStringValue``, ``fieldKeyStatus``, ``fieldKeyDataType``.
* InfluxDB default tag key name (``n``) is made configurable, using JSON option ``defaultTagName``.
* Updated to use the newer version of the JavaScript front-end library.


### Version 1.2.4 2020-Oct-19

* Fixed issue: Application crashes when receives POST request on in-complete OData URL.
* Fixed issue: Writing to InfluxDB stops when the numeric type variable's value, converted to float type, becomes equal to the special value ``infinity``.
* Added support to write special values for numeric type variables: ``min``, ``max``, ``inf``, ``nan``.
* For InfluxDB improved precision of written values: now numeric values are written as 64-bit float, before they were written as 32-bit float. 
* For InfluxDB, added configuration option which allows writing of numeric values of integer type without conversion to 64 bit float. 

### Version 1.2.3 2020-Sep-21

* Added new time-Series Database of ``Confluent`` type, used to connect to instances of Confluent Cloud or Confluent Enterprise.
* Re-built with the latest version of the C++ OPC UA Client SDK, with the following changes/fixes:

  * If an OPC UA Server returns ServiceFault response for the CloseSecureChannelRequest, it is not considered as an error anymore.
  * Fixed connectivity issue happening when OPC UA Server in the GetEndpoints response returns endpoint URL with host name which is not accessible from the machine where ogamma Visual Logger for OPC is running. For example, this might happen when the OPC UA server running in a docker container returns that container's host name in the endpoint URL. Now in such cases that host name is replaced by host name or IP address used in the original endpoint URL used to call the GetEndpoints service.

* Into the GitHub repository of the ogamma Visual Logger for OPC added file docker/kafka.yml, used to run Apache Kafka in a Docker container.
* Modified docker-compose configuration files in product's GitHub page: now they use specific versions of Docker images used in internal tests, instead of latest versions. This is done to eliminate cases when newer versions of images due to changes cause issues on interoperability with ogamma Visual Logger for OPC.
* Default key values for Apache Kafka is modified to empty string (before was "Unknown"). This behaviour can be changed by defining of the option ``default_key_value`` in the Json field.
* Fixed issue: writing variable values from Logged Variables table is handled as configuration change (i.e. OVL reconnects to the OPC UA Server).
* Updated User Manual: added section for Confluent, and some editing.

### Version 1.2.2 2020-Sep-12

* Modified default settings in the Json field for Apache Kafka type database connection configuration:

  * metadata.broker.list - now by default set to empty value. Values from fields Host and Port will be used as a connection URL. If this option is not empty, then its value will be used as connection URL, and values of fields Host and Port will be ignored.
  * batch.num.messages - removed. In Producer configuration, value of the field ``Write Batch Size`` is used for it. If this option is defined, then it is used, and value of the field ``Write Batch Size`` will be ignored. In consumer configuration, value of the field ``Read Batch Size`` used for it.
  * queue.buffering.max.ms - removed. Value of the field ``Max Write Interval`` will be used.

* Some default values for time-series database configuration settings changed to match with values set in Docker containers.
* docker-compose.yml file in product's GitHub repository is split into multiple files, so now it is possible to run selected subset of containers by changing arguments passed to the docker-compose command.

### Version 1.2.1 2020-Sep 7

* Fixed issue: The field ``Key Name Generation Mode`` is not visible when it should be according to the selected TSDB type in the Time-Series database configuration dialog window.
* Modified how default key value is generated for TSDB type ``Apache Kafka``: removed part ``n=`` from it.
* For TSDB types ``InfluxDB 2.0`` and ``InfluxDB 1.7`` added new option in JSON field: ``numberOfConnections``, to increase performance of writing values to the target database. As a result, now it is possible to write 100,000 values per second and more to the instance of InfluxDB database hosted in cloud, from instance of ogamma Visual Logger for OPC running in local network.
* For TSDS of InfluxDB type (all versions) improved handling of communication errors and fixed issue with invalid timestamps (which was causing InfluxDB return error 400, Bad Request).
* Minor change in the Login dialog window: now pressing Enter key when either Login or Password field is in focus is equivalent to clicking on the Login button.
* Added new feature to display some statistical data about application performance, accessible via menu ``Tools / Statistics``. 
* Minor improvement in the dialog window ``Time-sereis Database Configuration Settings``: when a new record is being edited, and in the field ``Type`` database type is selected, other fields are assigned default values, so no need to click on the button ``Reset to defaults``.
* For MQTT type databases, disabled using of the option ``persistType`` in the JSON field. As a result, the same in-memory buffer meachanizm is used for this type of database too, as for others.
* For Apache Kafka type databases, into the Json field added option ``Producer /  message.send.max.retries`` with default value 0, to eliminate retries by the underlying library (retries can be handled at the application level).
* Fixed issue: when time-series database type is ``Apache Kafka``, values for the column ``partition`` in the ``Logged Variables`` table are not read correctly after editing them.
* For InxluxDB 2.0 type database now connection token value can be saved in the ``Password`` field, in encrypted format. Before it was saved in the Json field's option ``token``. 
 
### Version 1.2.0 2020-Aug-04

* Added support to publish data to MQTT Broker. Verified with the following MQTT Brokers:
  * Eclipse Mosquitto
  * Microsoft Azure IoT Hub
  * AWS IoT Broker
  * Google Cloud IoT Core MQTT Bridge.

* Modified logic on connections to SQL family of TSDB databases: now if an attempt to check if the database exists and/or create it fails, this error is ignored. This allows us to connect with a user account with restricted permissions.
* Upgraded to use the newer version of the licensing library. As a result, installations with the older versions will require reactivation of the license key. The same keys should be re-used. 

### Version 1.1.1 2020-Jun-22

* Added support to store data in MemSQL database (uses the same client library as MySQL, with connection settings specific for MemSQL). 
* Added new feature: now all children variables from the node in the address space tree panel can be added using context menu. Note that the parent node should be expanded first.
* Improved performance on adding large number of variables from the address space.
* Fixed connectivity issue happening when OPC UA messages are large and split into chunks. One use case when it was happening is when number of logged variables per server connection exceeds 1000 or more tags.
* Fixed re-connection issue (in some cases was not able to establish connection to OPC UA Server after communication failure).


### Version 1.1.0 2020-Jun-06

* Added support to store data in Microsoft SQL as a time-series database.
* Added support to store data in MySQL as a time-series database.
* Added support to store data in SQLite as a time-series database.
* Default configuration database type and time-series database type in all distribution packages (Windows, Ubuntu, Docker) is set to SQLite type, so the instance is ready to use immediately without installing of additional database components.
* Improved handling of connection interruptions with the time-series database of PostgreSQL/TimescaleDB type.
* Fixed bug: in the case when a time-series database type is PostgreSQL, data values are written twice (was introduced in version 0.8.1).

### Version 1.0.1 2020-May-13

* Fixed issue: ActivateSession call fails at attempt to connect to KepServerEX, if connection security mode none-secured is used in combination with username/password type of user identity token.
* Fixed issue: Failes to connect to the configuration database of type PostgreSQL in encrypted mode;
* Fixed issue: Failes to connect to the time-series database of type PostgreSQL(TimescaleDB) in encrypted mode;
* Significantly improved performance of writing values to the time-series database when it's type is ``PostgreSQL``. As a result, now TimescaleDB/PostgreSQL database can be located not only in the local network, but also in the cloud too.
* Added feature to download application instance certificate as well as CA certificates and CRL via menu Settings / Download Certificate.
* Fixed issue: writing values to TimescaleDB/PostgreSQL or Apache Kafka might fail if data value has source timestamp not set or status code is bad.
* Licensing conditions for Community Edition changed: 
  * now on instances of the application which are activated after May 14, 2020 maximum number of logged variables is reduced to 64 after end of 1 month trial period. Existing installations activated before May 14, 2020 have limit as it was before: up to 256 variables.
  * periodic license validation with connection to the license server over the Internet is required. The date when the license was last time validated and the date before which the next validation should be performed are displayed in the dialog window opened via menu License / Status.
 

### Version 1.0.0 2020-Apr-29

* First production release.
* Role ``Collector Agent`` now can be disabled/enabled in dialog window used to edit application instances settings.  
* Fixed issue: If real time value of a variable is empty, it is displayed in Logged Variables table, column "value" as value "true" of boolean type.

### Version 0.9.1 2020-Apr-27

* Improved offline license activation workflow: now generated offline activation file can be downloaded via configuration GUI, and licence file can be uploaded via GUI too.
* Optimized license re-activation: now after entering activation key GUI is adjusted accordingly to expected action: activation or re-activation.
* Fixed error ``index out of range error`` reported by logging subsystem.
* Modifications in licensing to support Standard, Enterprise and Academic editions.
* In docker-compose.yml file added one more container: ``portainer/portainer``, the tool with web GUI to manage Docker environments. Portainer GUI is available at port 9000.
* Added support to pass name of configuration file in environment variable ``OVL_CONFIG_FILE``, which simplifies running multiple docker containers with ogamma Visual Logger for OPC.
* Added column ``Log to TSDB`` into the table ``Variable Groups``, for group of variables which should not be logged into time-series database by default. The aim is to simplify creation of records in the ``Logged Variables`` table which are used to serve queries from Grafana to read real time data directly from OPC UA Server.
* Adjusted feature ``Refresh Data`` to display last read values for variables, which are not logged into TSDB. (They are read directly from OPC UA Server to fulfill queries from Grafana).
* Rebuilt with newer version of the OPC UA SDK, with the following change: Message sequence numbers start from 1 after disconnection (to solve issue with CodeSys OPC UA Server).
* Fixed issue "ActivateSession request might fail when connections to multiple OPC UA Servers are created, due to using wrong identity token policy id".
* Fixed issue with high (~ 10% at low load) CPU usage.

### Version 0.9.0 2020-Apr-20

* More memory leaks fixed.
* Added support for https.
* Passwords in settings, used to connect to the configuration database or to time-series databases, now stored in encrypted fromat.
* Added user authentication feature to access configuration GUI, using simple built-in identity provider.
* Some cosmetic changes in GUI (added button to change width of the Address Space panel, separated buttons used to change OPC UA Server connection settings from Log button, added icons to main menu items).

### Version 0.8.7 2020-Mar-30

* Fixed issue: connection to the OPC UA Server is not restored after network connectivity issue.
* Fixed issue: when connection with OPC UA server is lost, ``Status`` column values in the ``Logged Variables`` table aren't changed to ``Bad``.
* Fixed issue: memory leak (was caused by in-memory debug logging accidentally left turned on).

### Version 0.8.6 2020-Mar-21

* Fixed issue: in some cases size of sent OPC UA message chunks exceeds negotiated limit, which causes closing of connection by the server side.
* Fixed issue: if target OPC UA server has multiple endpoints with UserName type Identity token, wrong security policy can be selected for password encryption, which causes failure of ActivateSessoin call with "User Identity token invalid" error.
* Fixed issue: fields in the OPC UA applicaton instance certificate does not match with ApplicationDescription structure sent to the server on CreateSession request, which causes connection failure if the server is configured to reject such requests.
* Fixed issue: if server returns in FindServers or GetEndpoints response endpoint URL with IP address different than in the original request and which is not accessible from network where ogamma Visual Logger for OPC instance is running, connection is not possible. This might happen for example if UA Server is accessed via VPN, or running in Docker container with IP address which is not accesible from external machines. To fix this issue, in-accessible IP address in the endpoint URL is substituted by original request's IP address. If server returns host name, connection is established too.
* Default value for number of threads in web server increased from 1 to 4, for better responsiveness.
* Fixed issue: application crashes when OPC UA Server or TSDB or Instance seetings are changed.
* Using newer version of the OPC UA Client SDK, with fixes for crash and deadlock issues. Also it uses larger OPC UA message chunk sizes by default.
* Revised and added more log messages for easier troubleshooting and diagnosys of possible issues.
* Earliest date for start of the 1 month trial period with enabled Enterprise Edition features in Community Edition of the product is moved from April 1, 2020 to May 1, 2020.
* Added experimental support for writing of values to OPC UA Server (by changing values in the ``Value`` field in the ``Logged Varaibles`` table).
* Fixed issue: if Apache Kafka is used as TSDB, values for fields ``Topic Name Generation Mode`` and ``Key Name Generation Mode`` set in the GUI ignored, instead values set in the ``Database specific settings / Json `` are used. Now values set in the Json fieid will be ignored.
* Fixed issue: when Apache Kafka is used as TSDB by the instance, saving changes of that TSDB record settings causes application crash.
* In the ``Logged Variables`` table value of the Refresh Data selector widget now is saved between browser sessions. 
* Fixed issue: Ubuntu version crashes due to incorrect using of licensing library.

### Version 0.8.5 2020-Mar-05

* Fixed issue: application log file size grows greater than set by the max. file size option.

### Version 0.8.4 2020-Mar-03

* Fixed issue: when there are multiple OPC UA Server connections configured in the address space, and there are multiple variable groups  with variables, and all of them are collapsed, and when group selection is changed, this causes infinite calls from browser to the backend. Can also cause application crash.
* Fixed issue: upgrade from older versions (prior 0.8.1) (Ubuntu and Docker versions) with configuration database of SQLite type does not completely upgrade tables, and does not report error.
* Upgraded some dependencies (web framework and ODB library) to newer versions.
* Docker image changed to stop container when application process stops.
* To support upgrades from older versions, when InfluxdB settings are loaded from ./data/config.json file, its mapping settings configured to be the same as in older versions (i.e. ``measurement`` will be set to ``d`` and tag will be set to ``n=[variable id]``).


### Version 0.8.3 2020-Feb-29

* Fixed issue: Application crashes at attempt to activate or re-activate license.
* Fixed issue: Instance configuration changes sometimes not saved or not applied without restart.
* To be consistent with older versions, for InfluxDb modified values set by button ``Reset to defaults`` to the same settings as in versions prior 0.8.1 (i.e. ``measurement`` will be set to ``d`` and tag will be set to ``n=[variable id]``).
* Improvements in logging messages formatting and runtime error handling.
* Ubuntu executable binary is built without debug info to reduce size.

### Version 0.8.2 2020-Feb-26

* Web server port number and number of threads now can be changed at runtime via menu ``Settings/Instances``.
* Fixed issue: application crashes if configuration database type is changed at runtime.
* Fixed issue: If more than one Collector Configuration is used, then in Grafana SimpleJson tag selector all variables from all configurations are displayed, while only those which belong to the configuration assigned to the instance should be displayed.
* Modified column names in Logged Variables table to match with time-series database type.
* Fixed issue: Column ``Status`` in ``Logged Variables`` table is writable, should be read only.
* Added text field displaying current instance name and ID.
* Fixed issue: in the Instances table link to open the instance page was not correct.

### Version 0.8.1 2020-Feb 23

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

### Version 0.7.1 2020-Jan-16

* Fixed issue of building address space tree in GUI, occurring when the same node is referred from multiple parent nodes.

### Version 0.7.0 2020-Jan-12

* Added support for licensing. Now application requires activation using license key, which can be obtained for Community Edition using One-Way Automation online store at https://onewayautomation.com/online-store. License can be activated via Web GUI (menu `Setup/License`).
* Improved error handling.
* Changes in configuration file, related to time-series database connections. now appied without re-start, at runtime.
* Fixed issue "Log files cannot be accessed via Web GUI on Windows".
* Fixed issue "Reading data from InluxDB to Grafana fails".
* In the Logged Variables grid added feature `Column Chooser` to show or hide columns.
* Added link to Release Notes into the `Help and Links` menu.
* Added link to open configuration settings into `Setup` menu (currently not enabled though).
* Improved handling of temporary disconnections from time-series databases: now failed write batch is kept in the in-memory queue and written when connection is restored, eliminating data lost. If time-series database is not available at start time, data also cached in memory buffer.


### Version 0.6.1 2020-Jan-01

* Maintenance release. Fixed runtime error issue (occurring when some fields in the Logged Variables table are edited).

### Version 0.6.0 2019-Dec-28

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

### Version 0.5.2 2019-Nov-09

* Added support for UserName identity token type on connections to OPC UA Servers;
* Added support for OPC UA deadband, so now data changes can be reported only when change of the value is greater than defined by deadband settings. 
* Re-build with the latest version of the OPC UA SDK, so now it can connect to OPC UA Servers running within containers, when Visual Logger is running outside of container, using host machines' name in endpoint URL.

### Version 0.5.1 2019-Nov-06

Fixed issue: was not connecting to InfluxDB in secured mode.

### Version 0.5.0 2019-Nov-02

* Added support for InfluxDB database (versions 1.7 and 2.0, https://www.influxdata.com/).
* Fixed bug: After restart, tries re-create TSDB database, but fails and exits, if OS language is not English.
* Web framework upgraded to the newest version;

### Version 0.4.2, 25 Aug, 2019

* Re-built with newer versions of dependencies;
* Added distribution package for Debian Stretch;
* Updated User Manual.
