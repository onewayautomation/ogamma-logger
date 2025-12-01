#!/bin/bash

# Exit on error
set -e

# ===== Configuration =====

PARENT_IF="enp2s0"
MACVLAN_IF="macvlan0"
CON_NAME="macvlan-host"

# Host-side macvlan IP (must be free)
HOST_IP="192.168.1.134/24"

# Container 1 macvlan IP (the only one we route)
CONTAINER1_IP="192.168.1.135"

# Docker bridge gateway (usually 172.17.0.1)
DOCKER_BRIDGE_GW="172.17.0.1"
DOCKER_BRIDGE_IF="docker0"

ACTION="${1:-create}"

# ===== FUNCTIONS =====

remove_connection() {
  echo "Removing macvlan connection..."

  # Remove route for the container
  if ip route show | grep -q "$CONTAINER1_IP"; then
    sudo ip route del "$CONTAINER1_IP" dev "$MACVLAN_IF" 2>/dev/null || true
    echo "Removed route for $CONTAINER1_IP"
  else
    echo "No route for $CONTAINER1_IP found"
  fi

  # Remove NetworkManager macvlan
  if nmcli connection show "${CON_NAME}" >/dev/null 2>&1; then
    sudo nmcli connection delete "${CON_NAME}"
    echo "Connection ${CON_NAME} removed"
  else
    echo "Connection ${CON_NAME} does not exist"
  fi

  # Bring interface down if exists
  if ip link show "$MACVLAN_IF" >/dev/null 2>&1; then
    sudo ip link set "$MACVLAN_IF" down || true
    sudo ip link delete "$MACVLAN_IF" || true
    echo "Interface $MACVLAN_IF removed"
  fi

  echo "Removal done."
}

create_connection() {
  echo "Creating persistent macvlan host interface..."

  echo "[1/6] Removing any existing connection..."
  sudo nmcli connection delete "${CON_NAME}" 2>/dev/null || true

  echo "[2/6] Creating macvlan interface..."
  sudo nmcli connection add type macvlan \
    ifname "${MACVLAN_IF}" \
    dev "${PARENT_IF}" \
    mode bridge \
    con-name "${CON_NAME}" \
    ipv4.method manual \
    ipv4.addresses "${HOST_IP}" \
    ipv4.never-default yes

  echo "[3/6] Activating connection..."
  sudo nmcli connection up "${CON_NAME}"

  echo "[4/6] Adding SAFE route ONLY for Container 1..."
  # Route only the macvlan container, not the whole subnet
  sudo ip route replace "$CONTAINER1_IP" dev "${MACVLAN_IF}"

  echo "[5/6] Verifying interface and routing..."
  ip addr show "${MACVLAN_IF}"
  ip route | grep "$MACVLAN_IF" || true

  echo "[6/6] Testing connectivity to Container 1..."
  echo "Testing ping (may fail if container is not running)..."
  ping -c 1 "$CONTAINER1_IP" || true

  echo "Macvlan interface setup complete."
  echo "Container 2 should now be able to reach $CONTAINER1_IP"
}

# ===== MAIN =====

case "${ACTION}" in
  remove)
    remove_connection
    ;;
  create|"")
    create_connection
    ;;
  *)
    echo "Usage:"
    echo "  $0          # create macvlan interface"
    echo "  $0 remove   # remove macvlan interface"
    exit 1
    ;;
esac
