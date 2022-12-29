import os
import binascii
import paho.mqtt.client as mqtt
import logging
# Eclipse Paho MQTT Python client library
# https://pypi.org/project/paho-mqtt/
# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php


# QOS 0 messages are fire and forget so there is no acknowledgment and
# thus no message ID is needed. The spec states "A PUBLISH Packet
# MUST NOT contain a Packet Identifier if its QoS value is set to 0.".

logger = logging.getLogger(__name__)

# Execute the specified command for a door


def execute_command(door, command):
    doorName = door.name
    logger.info("Executing command %s for door %s", command, doorName)
    if command == "OPEN" and door.state == 'closed':
        door.open()
    elif command == "CLOSE" and door.state == 'open':
        door.close()
    elif command == "STOP":
        door.stop()
    else:
        logger.info("Invalid command: %s", command)


class MQTT_Helper(object):
    def __init__(self, config, door):
        self.door = door
        host = config['mqtt']['host']
        port = int(config['mqtt']['port'])
        user = config['mqtt']['user']
        password = config['mqtt']['password']
        discovery = bool(config['mqtt'].get('discovery'))
        if 'discovery_prefix' not in config['mqtt']:
            discovery_prefix = 'homeassistant'
        else:
            discovery_prefix = config['mqtt']['discovery_prefix']

        clientID = "MQTTGarageDoor_" + str(binascii.b2a_hex(os.urandom(6)) )
        self.mqttc = mqtt.Client(client_id=clientID,
                                 clean_session=True, userdata=None, protocol=4)

        # Uncomment to enable debug messages
        #mqttc.on_log = on_log

        # set topic
        if discovery is True:
            base_topic = discovery_prefix + "/cover/" + str( door.id )
            config_topic = base_topic + "/config"
            config['command_topic'] = base_topic + "/set"
            config['state_topic'] = base_topic + "/state"

        self.command_topic = config['command_topic']
        self.state_topic = config['state_topic']
        logger.info("set self.command_topic=", self.command_topic)
        logger.info("set self.state_topic=", self.state_topic)

        # Assign event callbacks
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.message_callback_add(self.command_topic, self.on_message)

        #  Last Will & Testament feature is used by the MQTT client to tell the broker to publish a pre-defined message if the client disconnects.
        self.mqttc.will_set(
            self.state_topic, payload="offline", qos=0, retain=True)

        # connect
        self.mqttc.username_pw_set(user, password=password)
        self.mqttc.connect(host, port, 60)

        # You can add additional listeners here and they will all be executed when the door state changes
        self.door.onStateChange.addHandler(self.on_state_change)

        # Publish initial door state
        self.mqttc.publish(self.state_topic, door.state, retain=True)

        # If discovery is enabled publish configuration
        if discovery is True:
            self.mqttc.publish(config_topic, '{"name": "' + door.name + '", "command_topic": "' +
                               self.command_topic + '", "state_topic": "' + self.state_topic + '"}', retain=True)
    ################
    # Define event callbacks

    # callback when the client receives a CONNACK response from the server.
    # When paho disconnects and connects again, it won't resubscribe automatically.
    # That's why subscriptions should be made in the on_connect callback.

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected with result code: %s", mqtt.connack_string(rc))
        logger.info("Listening for commands on %s", self.command_topic)
        # Start subscribe, with QoS level 0
        self.mqttc.subscribe(self.command_topic,
                             payload="online", qos=0, retain=True)

    # callback when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        logger.info("on_message "+str(msg))
        execute_command(self.door, str(msg.payload))

    # callback when a message that was to be sent using the publish() call has
    # completed transmission to the broker.
    # This callback is important because even if the publish() call returns
    # success, it does not always mean that the message has been sent.
    def on_publish(self, client, userdata, mid):
        logger.info("on_publish mid: " + str(mid))

    # callback when the broker responds to a subscribe request.
    def on_subscribe(self, client, obj, mid, granted_qos):
        logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, client, userdata, level, buf):
        logger.info("on_log:"+str(buf))

    # Callback per door that passes the doors state topic
    def on_state_change(self, value, topic=None):
        logger("State change triggered: %s -> %s", topic, value)
        # Update the mqtt state topic
        if topic == None:
            topic = self.state_topic
        self.mqttc.publish(topic, value, retain=True)

# Continue the network loop, exit when an error occurs
# rc = 0
# while rc == 0:
#     rc = mqttc.loop()
# logger.info("rc: " + str(rc))
