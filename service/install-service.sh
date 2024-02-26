#!/bin/bash

# Copy the config to the systemd folder.
sudo cp ./ascenseur.service /etc/systemd/system/ascenseur.service

# Then, enable the service.
sudo systemctl daemon-reload
sudo systemctl enable ascenseur.service
