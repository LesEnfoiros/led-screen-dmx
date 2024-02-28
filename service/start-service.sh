#!/bin/bash
#
# This software starts the service after cleaning
# the previous files.
#
# Author: Damien MOLINA

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Redirect the output of this script in a log file.
exec >> $CURRENT_DIR/log/`date +%Y%m%d`.log
exec 2>&1

# Let's mark this as a new execution of the script.
echo "======================================"
date
echo "======================================"

# Clean the service folder from socket files.
rm $CURRENT_DIR/*.socket

# And... execute the script.
sudo python3 $CURRENT_DIR/../python/main.py 