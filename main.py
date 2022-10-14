"""
target version Python 3.9.2
"""
import os
import json
from controller import Controller

config_filename = "config.json"

# "mqtt": {
#     "host": "host",
#     "port": "port",
#     "user": "user",
#     "password": "password",
#     "discovery": "true",
#     "discovery_prefix": "homeassistant",
#     "state_topic": "home-assistant/cover",
#     "command_topic": "home-assistant/cover/set"
# },

# The callback for when the client receives a CONNACK response from the server.


def parseConfig():
    config_file = open(config_filename)
    data = json.load(config_file)
    config_file.close()
    return data


def main():
    configs = parseConfig()
    controller = Controller(configs)
    controller.run()


if __name__ == '__main__':
    print("Welcome to GarageDoorAdmin")
    main()
