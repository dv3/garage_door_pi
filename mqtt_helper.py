import os
import binascii
import paho.mqtt.client as mqtt

# Eclipse Paho MQTT Python client library
# https://pypi.org/project/paho-mqtt/
# https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php


class MQTT_Helper(object):
    def _init__(self, config):
        host = config['mqtt']['host']
        port = int(config['mqtt']['port'])
        user = config['mqtt']['user']
        password = config['mqtt']['password']
        discovery = bool(config['mqtt'].get('discovery'))
        if 'discovery_prefix' not in config['mqtt']:
            discovery_prefix = 'homeassistant'
        else:
            discovery_prefix = config['mqtt']['discovery_prefix']

        clientID = "MQTTGarageDoor_" + binascii.b2a_hex(os.urandom(6))
        self.mqttc = mqtt.Client(client_id=clientID,
                                 clean_session=True, userdata=None, protocol=mqtt.MQTTv31)

        # Assign event callbacks
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_publish = self.on_publish
        self.mqttc.on_subscribe = self.on_subscribe

        # Uncomment to enable debug messages
        #mqttc.on_log = on_log

        # set topic
        if discovery is True:
            base_topic = discovery_prefix + "/cover/" + config['door']['name']
            config_topic = base_topic + "/config"
            config['command_topic'] = base_topic + "/set"
            config['state_topic'] = base_topic + "/state"

        self.command_topic = config['command_topic']
        self.state_topic = config['state_topic']

        # connect
        self.mqttc.username_pw_set(user, password=password)
        self.mqttc.connect(host, port, 60)

        # Publish a message
        self.mqttc.publish(self.command_topic, "First message")

    # Define event callbacks

    # callback when the client receives a CONNACK response from the server.
    # When paho disconnects and connects again, it won't resubscribe automatically.
    # That's why subscriptions should be made in the on_connect callback.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code: %s", mqtt.connack_string(rc))
        print("Listening for commands on %s", self.command_topic)
        # Start subscribe, with QoS level 0
        self.mqttc.subscribe(self.command_topic, 0)

    # callback when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    # callback when a message that was to be sent using the publish() call has
    # completed transmission to the broker.
    # This callback is important because even if the publish() call returns
    # success, it does not always mean that the message has been sent.
    def on_publish(self, client, userdata, mid):
        print("mid: " + str(mid))

    # callback when the broker responds to a subscribe request.
    def on_subscribe(self, client, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(self, client, userdata, level, buf):
        print(buf)

# Continue the network loop, exit when an error occurs
# rc = 0
# while rc == 0:
#     rc = mqttc.loop()
# print("rc: " + str(rc))
