# garage_door_pi

## Requirements

overall requirement:
- don't break garage opener
- don't break standard remote
- don't break wall mounted remote
- integrate with home assistant
- standalone incase home assistant if offline

html webpage:
- current snapshot
- current door status
- reload photo button
- open/close door button
- access old snapshot extra
- video extra
- control light extra

home assistant integration:
- current door status
- open/close door button
- current snapshot
- reload photo button
- video extra
- control light extra

Technical requirement:
- mqtt
- webpage

## Config


## magnetic reed switch
black : NC
brown : NO to GPIO input
white : COM to GND

N.C. means Normally Closed: 
When the magnet together, the circuit is conductive( light on ); 
When the magnet separates, the circuit is not conductive ( light off );
N.O. means Normally Open: 
When the magnet separates, the circuit is conductive( light on );
When the magnet together, the circuit is not conductive ( light off ).

https://www.amazon.com/Switch-Normally-Closed-Sensor-Applicable/dp/B07YW47395/ref=cm_cr_arp_d_product_top?ie=UTF8

## Two channel relay
The relay module has two LEDs that indicate the status of the relay. When a relay is activated, the corresponding LED lights up.

Control Pins:
VCC pin provides power to the built-in optocouplers and, optionally, the relay’s electromagnet (if you keep the jumper in place). Connect it to the 5V pin on the Arduino.
IN1 & IN2 pins control the relay. These are active low pins, which means that pulling them LOW activates the relay and pulling them HIGH deactivates it.
Power Supply Selection Pins:
JD-VCC provides power to the relay’s electromagnet. When the jumper is in place, JD-VCC is shorted to VCC, allowing the electromagnets to be powered by the Arduino’s 5V line. Without the jumper cap, you’d have to connect it to a separate 5V power source.
VCC pin is shorted to the JD-VCC pin with the jumper cap on. Keep this pin disconnected if you remove the jumper.
Output Terminals:
COM terminal connects to the device you intend to control.
NC terminal is normally connected to the COM terminal, unless you activate the relay, which breaks the connection.
NO terminal is normally open, unless you activate the relay that connects it to the COM terminal.

https://lastminuteengineers.com/two-channel-relay-module-arduino-tutorial/

## OS Raspbian
Run pinout command

## Software

## Dependencies
- Raspberry pi 1
- Python 3.x
- pip

## Installation  
- git clone https://github.com/dv3/garage_door_pi.git
- pip install -r requirements.txt
- edit the configuration.yaml to set up mqtt (See below)
- python main.py
- To start the server on boot run sudo bash autostart_systemd.sh
python -u /home/pi/garage_door_pi/main.py

## MQTT Mosquitto broker:

#### Home Assistant
status_topic: 'homeassistant/status'
discovery_topic: 'homeassistant'
server: 'mqtt://core-mosquitto:1883'
base_topic: zigbee2mqtt

#### Standalone
In separate terminal windows do the following:

download mosquitto broker:
https://mosquitto.org/download/

Start the broker:
mosquitto
Start the command line subscriber:

mosquitto_sub -v -t 'test/topic'
Publish test message with the command line publisher:

mosquitto_pub -t 'test/topic' -m 'helloWorld'

------------
Links:
https://www.switchedonnetwork.com/2018/06/25/smart-letterbox-push-notifications-raspberry-pi-zero/
https://www.ryansouthgate.com/2015/08/10/raspberry-pi-door-sensor/

https://github.com/shawn-peterson/GarageDoorPi
https://github.com/andrewshilliday/garage-door-controller
https://github.com/jerrod-lankford/GarageQTPi
https://jpowcode.github.io/http_to_mqtt.html
https://github.com/maddox/harmony-api
https://github.com/nebhead/garage-zero
https://www.driscocity.com/idiots-guide-to-a-raspberry-pi-garage-door-opener/
https://github.com/ide/pico-garage-door-sensor/blob/main/src/debounce.py
https://github.com/shrocky2/SiriGarage

https://python-hassdevice.readthedocs.io/en/stable/_modules/hassdevice/devices.html
https://gyandeeps.com/garage-operations-raspberrypi/

https://core-electronics.com.au/projects/wifi-garage-door-controller-with-raspberry-pi-pico-w-smart-home-project/
https://github.com/geerlingguy/pico-w-garage-door-sensor/tree/2d8f9dbb9d9e091c77c314781c34cf07a701e2f1/micropython
https://renjithn.com/garagepi-garage-opener-using-raspberry-pi/
https://github.com/julienfouilhe/automate-gate-opening
https://www.instructables.com/Raspberry-Pi-Garage-Door-Opener-with-streaming-vid/
