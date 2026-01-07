# Running Confluent services in Docker

Original Docker compose files are based on the file ``cp-all-in-one/docker-compose.yml`` at Git repository https://github.com/confluentinc/cp-all-in-one.git.

Services from the original file ``docker-compose.yml`` were split into 2 files to have ability to start the ``connect`` service independently from the ``broker`` and other services:

  - ``confluent-connector.yml`` with service ``connect``, with modifications run OPC UA Kafka Source Connector from One-Way Automation. Note that the OPC UA Source Connector jar file is not included in this repository, it needs to be downloaded from this link: https://onewayautomation.com/opcua-binaries/OpcUaKafkaSourceConnector-1.0.0-4.2.2.jar to the sub-folder ``docker/custom-connectors`` of the repository root folder.
  - ``confluent.yml`` with the rest of Docker services. the ``broker`` service is modified to persist its state in Docker volume ``kafks-data``.

These Docker Compose configuration files should be started from working directory set to sub-folder ``docker`` of this Git repository:

```
docker compose -f confluent/confluent.yml up -d
docker compose -f confluent/confluent-connect.yml up -d
```

Once Confluent containers complete start-up, Control Center GUI will be available at http://localhost::9021. 

OPC UA Kafka Source Connector instances can be managed (created, modified, restarted, deleted) via Confluent Control Panel: in the left side panel, select menu ``Connect``, then select Connect Cluster in the center panel. From there, you can manage connector instances.

Sample configuration follows below:

```
{
  "name": "opcua",
  "config": {
    "connector.class": "com.opcfy.logger.kafka.OpcUaKafkaSourceConnector",
    "opcua.connector.work.dir": "/home/appuser/opcua",
    "opcua.connector.out.topic": "ovl-console",
    "opcua.connector.ha.out.topic": "ha-console",
    "opcua.connector.healthcheck.enabled": "true",
    "opcua.connector.check.process.on.start": "true",
    "opcua.connector.wait.process.stop.timeout.ms": "60000",
    "opcua.connector.ha.cluster.enabled": "true",
    "opcua.connector.ha.cluster.id": "my-ovl-cluster-demo",
    "opcua.connector.ha.node.id": "node-1",
    "opcua.connector.ha.db.host.name": "192.168.1.89",
    "opcua.connector.ha.db.user": "ogamma",
    "opcua.connector.ha.db.password": "ogamma",
    "opcua.connector.ha.db.name": "ovlha"
  }
}
```