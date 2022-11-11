#!/usr/bin/python3

"""
target version Python 3.9.2
"""
import logging
import json
from controller import Controller
from garage_door import GarageDoor
from mqtt_helper import MQTT_Helper

config_filename = "config.json"
log_filename = "garage_opener.log"
logger = logging.getLogger(__name__)


def setup_logger():
    # set gloabl logger
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    # json.dumps
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


def parseConfig():
    config_file = open(config_filename)
    data = json.load(config_file)
    config_file.close()
    return data


def main():
    setup_logger()
    logger.info("starting main()")
    configs = parseConfig()
    door1 = GarageDoor(configs['door'])
    mqtt_client = MQTT_Helper(configs, door1)
    try:
        # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a manual interface.
        mqtt_client.loop_forever()
        # app = Flask(__name__)
        # app.run(host='0.0.0.0', debug=False)
        #from my_app import create_app
        #app = create_app()
    except KeyboardInterrupt:
        mqtt_client.disconnect()
    finally:
        mqtt_client.disconnect()
        # conn.close()


if __name__ == '__main__':
    print("Welcome to GarageDoorAdmin")
    main()
