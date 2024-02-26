#!/bin/bash

NETWORK_INTERFACE=wlp2s0

# Get the network range.
# See: https://stackoverflow.com/questions/59649346/extract-network-range-and-subnet-of-an-interface-from-a-linux-machine
NETWORK_RANGE=$(ip -o a | grep -oP "$NETWORK_INTERFACE\s+inet\s+\K\d+\.\d+\.\d+\.\d+/\d+")
echo "[INFO] Network range is:" $NETWORK_RANGE

# Execute nmap to find the device.
(nmap -sn $NETWORK_RANGE | grep pi) || echo "[ERROR] Raspberry card not found"