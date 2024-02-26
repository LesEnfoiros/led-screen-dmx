#!/bin/bash

# Redirect the output of this script in a log file.
exec >> log/`date +%Y%m%d`.log
exec 2>&1

# Let's mark this as a new execution of the script.
echo "======================================"
date
echo "======================================"

# And... execute the script.
sudo python3 main.py 