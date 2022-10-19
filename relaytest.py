#!/usr/bin/python3


import time
import RPi.GPIO as GPIO

print("Control + C to exit Program")

GPIO.setmode(GPIO.BOARD)    # the pin numbers refer to the board connector not the chip
GPIO.setwarnings(False)
# sets the pin input/output setting to OUT
# sets the pin output to high
GPIO.setup(23, GPIO.OUT)			#Door 1 Relay to Open Door
GPIO.output(23, GPIO.HIGH)
GPIO.setup(24, GPIO.OUT)		#Door 2 Relay to Open Door
GPIO.output(24, GPIO.HIGH)
GPIO.setup(15, GPIO.OUT)		#Not Used for the project
GPIO.output(15, GPIO.HIGH)



try:
  while 1 >=0:
    GPIO.output(23, GPIO.LOW)   # turns the first relay switch ON
    time.sleep(.5)             # pauses system for 1/2 second
    GPIO.output(23, GPIO.HIGH)  # turns the first relay switch OFF
    GPIO.output(24, GPIO.LOW)  # turns the second relay switch ON
    time.sleep(.5)
    GPIO.output(24, GPIO.HIGH)    
    GPIO.output(15, GPIO.LOW)
    time.sleep(.5)
    GPIO.output(15, GPIO.HIGH)
    time.sleep(.5)

except KeyboardInterrupt:     # Stops program when "Control + C" is entered
  GPIO.cleanup()               # Turns OFF all relay switches