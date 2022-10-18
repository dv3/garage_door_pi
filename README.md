# garage_door_pi

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
----------
Config:
# normally_closed is 0, normally open is 1
state_pin_closed_value: 0

-----------
Mosquitto broker:

In separate terminal windows do the following:

Start the broker:

mosquitto
Start the command line subscriber:

mosquitto_sub -v -t 'test/topic'
Publish test message with the command line publisher:

mosquitto_pub -t 'test/topic' -m 'helloWorld'

------------
Links:
https://github.com/andrewshilliday/garage-door-controller
https://github.com/jerrod-lankford/GarageQTPi
https://jpowcode.github.io/http_to_mqtt.html
https://github.com/maddox/harmony-api

https://python-hassdevice.readthedocs.io/en/stable/_modules/hassdevice/devices.html

https://core-electronics.com.au/projects/wifi-garage-door-controller-with-raspberry-pi-pico-w-smart-home-project/
https://github.com/geerlingguy/pico-w-garage-door-sensor/tree/2d8f9dbb9d9e091c77c314781c34cf07a701e2f1/micropython
https://renjithn.com/garagepi-garage-opener-using-raspberry-pi/
https://github.com/julienfouilhe/automate-gate-opening
https://www.instructables.com/Raspberry-Pi-Garage-Door-Opener-with-streaming-vid/
