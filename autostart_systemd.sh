#!/bin/bash
cp garagemqttpi.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/garagemqttpi.service
sudo systemctl daemon-reload
sudo systemctl enable garagemqttpi.service
sudo systemctl start garagemqttpi.service
