#!/usr/bin/python3
#
import time
import random
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

host = 'core-mosquitto'
port = 1883
state_topic = 'homeassistant/status'
delay = 5
user = 'addons'
password = 'ahrahzaing1yoo9iexaW6xaeYei3eiphae4quaeZ4ahphoi8diph3ohN3Hae5oQu'

# Send messages in a loop
client = mqtt.Client("ha-client")
client.username_pw_set(user, password=password)
client.connect(host, port, 60)
client.loop_start()

# Send a single message to set the mood
#publish.single('home-assistant/status/mood', 'good', hostname=host)

while True:
    client.publish(state_topic, random.randrange(0, 50, 1))
    time.sleep(delay)