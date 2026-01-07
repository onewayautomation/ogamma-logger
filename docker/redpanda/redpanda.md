# Setting up Redpanda broker and OPC UA Source Connector.

## Redpanda broker

Single broker of Redpanda can be started using docker compose configuratino file ``redpanda.yml``, which was created following steps from this link: https://docs.redpanda.com/redpanda-labs/docker-compose/single-broker/

To start the container, run command:

```
docker compose -f redpanda/redpanda.yml up -d
```

## OPC UA Kafka Connector 

To start the OPC UA Kafka Connector, Docker compose configuration file ``redpanda-connect.yml`` can be used. This file is composed based on this web page from Redpanda: https://docs.redpanda.com/current/deploy/kafka-connect/deploy-kafka-connect/

Note that port number of the connector API endpoint is mapped to the host port ``8084`` instead of default port 8083.

Note that the OPC UA Source Connector jar file is not included in this repository, it needs to be downloaded from this link: https://onewayautomation.com/opcua-binaries/OpcUaKafkaSourceConnector-1.0.0-4.2.2.jar to the sub-folder ``docker/custom-connectors`` of the repository root folder.

To start, in terminal with workign directory set to the sub-folder ``docker`` of the repository folder, run the command:

```
docker compose -f redpanda/redpanda-connect.yml up -d
```

### Creating Kafka Connector Task for OPC UA

This can be done by REST call to the standard Kafka Connector API endpoint:

```
curl "localhost:8084/connectors" \
  -H 'Content-Type: application/json' \
  --data @redpanda/redpanda-connector-config.json
```

After running of the command, new connector task should be created.
To get list of connectors, run the command:

```
curl localhost:8084/connectors
```

### Get status of the specific connector

```
curl localhost:8084/connectors/opcua-connector/status
```
Here ``opcua-connector``is connector name.

### Delete connector

```
curl "localhost:8084/connectors/opcua-connector" -X 'DELETE'
```
