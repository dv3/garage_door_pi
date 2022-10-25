#!/usr/bin/python3
import time
import RPi.GPIO as GPIO

# The door sensor has two wires – connect 1 wire 
# (doesn’t matter which) to a free pin (I chose PIN 8 – 
# you need to refer to this PIN in the code explicitly) 
# and the other to one of the ground (GND) Pin

print("Control + C to exit Program")

GPIO.setmode(GPIO.BOARD)    # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
# sets the pin input/output setting to OUT
# sets the pin output to high

pin_num=16
GPIO.setup(pin_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(pin_num):
            print("Door is open")
            time.sleep(2)
        if GPIO.input(pin_num) == False:
            print("Door is closed")
            time.sleep(2)
except KeyboardInterrupt:     # Stops program when "Control + C" is entered
  GPIO.cleanup()               # Turns OFF all relay switches