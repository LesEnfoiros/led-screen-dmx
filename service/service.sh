#!/bin/bash
# This program interacts with the service running.
#
# Author: Damien MOLINA

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Get arguments from command line.
ARGS=$@

# Get the port from the file name.
FILES=( /tmp/*.socket )
SOCKET_FILE=$(basename -- "${FILES[0]}")
PORT="${SOCKET_FILE%.*}"

echo "[INFO] Contacting port $PORT"

# And execute the command given by the user.
(
    echo $ARGS
    sleep 0.2
) | nc localhost $PORT 2> /dev/null