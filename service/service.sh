#!/bin/bash
# This program interacts with the service running.
#
# Author: Damien MOLINA

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Get arguments from command line.
ARGS=$@

# Get the port from the file name.
FILES=( $CURRENT_DIR/*.socket )
SOCKET_FILE=$(basename -- "${FILES[0]}")
PORT="${SOCKET_FILE%.*}"

# And execute the command given by the user.
(
    echo $ARGS
    sleep 0.2
) | telnet localhost $PORT 2> /dev/null