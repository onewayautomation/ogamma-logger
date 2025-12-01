#!/bin/bash

# Detect docker or podman
dc=docker
if command -v podman &>/dev/null; then
  dc=podman
fi

# --------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------

INTERFACE="enp2s0"                # Physical NIC used for macvlan parent
MACVLAN_NET="ogamma-logger-m"     # Name of macvlan network
SUBNET="192.168.1.0/24"
IP_RANGE="192.168.1.128/25"

# --------------------------------------------------------------------
# FUNCTION: Create macvlan network
# --------------------------------------------------------------------

create_network() {

  # Validate interface
  if ! ip link show "$INTERFACE" &>/dev/null; then
    echo "Error: Interface '$INTERFACE' not found."
    exit 1
  fi

  echo "Creating macvlan network: $MACVLAN_NET"

  $dc network create -d macvlan \
    --subnet=$SUBNET \
    --ip-range=$IP_RANGE \
    -o parent=$INTERFACE \
    $MACVLAN_NET

  if ! $dc network inspect $MACVLAN_NET &>/dev/null; then
    echo "Error: Failed to create macvlan network."
    exit 1
  fi

  echo "macvlan network '$MACVLAN_NET' created successfully."
  echo "Bridge containers can reach macvlan containers via the host macvlan interface."
}

# --------------------------------------------------------------------
# FUNCTION: Remove macvlan network
# --------------------------------------------------------------------

remove_network() {

  echo "Removing macvlan network: $MACVLAN_NET..."
  if $dc network inspect $MACVLAN_NET &>/dev/null; then
    $dc network rm $MACVLAN_NET
    echo "macvlan network removed."
  else
    echo "Network not found, skipping."
  fi

  echo "Cleanup completed."
}

# --------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------

if [ "$1" == "remove" ]; then
  remove_network
else
  create_network
fi
