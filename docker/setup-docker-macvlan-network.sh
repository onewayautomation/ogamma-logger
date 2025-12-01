#!/bin/bash

# Function to create the macvlan network
create_network() {
  INTERFACE="enp2s0"  # Modify this to the correct interface name if necessary

  # Check if the interface exists
  if ! ip link show "$INTERFACE" &>/dev/null; then
    echo "Error: Interface '$INTERFACE' not found."
    exit 1
  fi

  NETWORK_NAME="ogamma-logger-m"
  SUBNET="192.168.1.0/24"
  GATEWAY="192.168.1.1"
  IP_RANGE="192.168.1.128/25"

  echo "Creating macvlan network: $NETWORK_NAME"
  podman network create -d macvlan \
    --subnet=$SUBNET \
    --gateway=$GATEWAY \
    --ip-range=$IP_RANGE \
    -o parent=$INTERFACE \
    $NETWORK_NAME

  # Verify that the network was created successfully
  if podman network inspect $NETWORK_NAME &>/dev/null; then
    echo "macvlan network '$NETWORK_NAME' created successfully."
  else
    echo "Error: Failed to create macvlan network."
    exit 1
  fi
}

# Function to remove the macvlan network
remove_network() {
  NETWORK_NAME="ogamma-logger-m"

  # Check if the network exists
  if podman network inspect $NETWORK_NAME &>/dev/null; then
    echo "Removing macvlan network: $NETWORK_NAME"
    podman network rm $NETWORK_NAME

    # Verify that the network was removed successfully
    if ! podman network inspect $NETWORK_NAME &>/dev/null; then
      echo "macvlan network '$NETWORK_NAME' removed successfully."
    else
      echo "Error: Failed to remove macvlan network."
      exit 1
    fi
  else
    echo "Error: Network '$NETWORK_NAME' does not exist."
    exit 1
  fi
}

# Check command-line argument
if [ "$1" == "remove" ]; then
  remove_network
else
  create_network
fi
