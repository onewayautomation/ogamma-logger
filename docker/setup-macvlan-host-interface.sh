#!/bin/bash

# Exit immediately if any command fails to avoid partially applied configuration
set -e

# ===== Configuration =====
PARENT_IF="enp2s0"
MACVLAN_IF="macvlan0"
CON_NAME="macvlan-host"

HOST_IP="192.168.1.134/24"
CONTAINER_IP="192.168.1.131"
SUBNET="192.168.1.0/24"
METRIC="50"
# =========================

ACTION="${1:-create}"

remove_connection() {
  echo "Removing macvlan connection..."

  if nmcli connection show "${CON_NAME}" >/dev/null 2>&1; then
    sudo nmcli connection delete "${CON_NAME}"
    echo "Connection ${CON_NAME} removed"
  else
    echo "Connection ${CON_NAME} does not exist"
  fi
}

create_connection() {
  echo "Creating persistent macvlan connection..."

  echo "[1/6] Removing existing connection if present..."
  sudo nmcli connection delete "${CON_NAME}" 2>/dev/null || true

  echo "[2/6] Creating macvlan connection..."
  sudo nmcli connection add type macvlan \
    ifname "${MACVLAN_IF}" \
    dev "${PARENT_IF}" \
    mode bridge \
    con-name "${CON_NAME}" \
    ipv4.method manual \
    ipv4.addresses "${HOST_IP}" \
    ipv4.never-default yes

  echo "[3/6] Adding static route with low metric..."
  sudo nmcli connection modify "${CON_NAME}" \
    +ipv4.routes "${SUBNET} 0.0.0.0 ${METRIC}"

  echo "[4/6] Bringing connection up..."
  sudo nmcli connection up "${CON_NAME}"

  echo "[5/6] Forcing route priority..."
  sudo ip route replace 192.168.1.0/24 dev "${MACVLAN_IF}" metric "${METRIC}"

  echo "[6/6] Showing interface and routes..."
  ip addr show "${MACVLAN_IF}"
  ip route | grep "${MACVLAN_IF}" || true

  echo "Done. You should now be able to ping ${CONTAINER_IP}"
}

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
