#!/usr/bin/python3
import time
import RPi.GPIO as GPIO

# The door sensor has two wires – connect 1 wire 
# (doesn’t matter which) to a free pin (I chose PIN 8 – 
# you need to refer to this PIN in the code explicitly) 
# and the other to one of the ground (GND) Pin

print("Control + C to exit Program")

# The input GPIO pins the Reed Switch is connected to for each door.
switch_pin = 17 		

try:
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)
    # GPIO 17 (11)
    GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # the pin numbers refer to the board connector not the chip
    # GPIO.setmode(GPIO.BOARD)
    # GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # GPIO 18, Pin 12 (RasPi Header)
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

    while True:
        if GPIO.input(switch_pin):
            print("Door is open")
            time.sleep(2)
        if GPIO.input(switch_pin) == False:
            print("Door is closed")
            time.sleep(2)
except KeyboardInterrupt:     # Stops program when "Control + C" is entered
  GPIO.cleanup()               # Turns OFF all relay switches