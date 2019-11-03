#!/bin/bash

# First, start InfluxDB in background:
if [ "$1" == "n" ]; then
	echo "Option n is passed, not running influxd"
else
	influxd &
fi

# Second, if not initialized yet (which we judge based on presense of the file), do initialization.
if [ ! -f /opt/influxdb2_initialized.txt ]; then
	if [ "$1" == "n" ]; then
		echo ""
	else
		# Let the service some time to start:
		echo "Waiting for influxd daemon to start before initializing Influx DB 2.0 ..."
		sleep 10
	fi
	echo "Initializing Influx DB 2.0 ..."
	influx setup -f --username ogamma --password ogamma123 --org ogamma --bucket ogamma --token secrettoken
	if [ $? -eq 0 ]; then
		echo "InfluxDB 2.0 successfully initialized."
		touch /opt/influxdb2_initialized.txt
	else
		echo "Failed to initialize InfluxDB 2.0. Please connect to the container and initialize it manually by running command [influx setup]"
	fi
else
	echo "File /opt/influxdb2_initialized.txt exists, so assuming that InfluxDB 2.0 should be initialized."
fi

# At the end, keep container running:
tail -f /dev/null
