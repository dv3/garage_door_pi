#!/usr/bin/python3
#
import time
import random
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

host = '192.168.0.100'
port=1883
state_topic = 'homeassistant/status'
delay = 5

# Send a single message to set the mood
publish.single('home-assistant/status/mood', 'good', hostname=host)

# Send messages in a loop
client = mqtt.Client("ha-client")
client.connect(host, port, 60)
client.loop_start()

while True:
    client.publish(state_topic, random.randrange(0, 50, 1))
    time.sleep(delay)