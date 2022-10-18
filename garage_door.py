#!/usr/bin/python3

import time
import RPi.GPIO as gpio
import logging
import sys
from eventhook import EventHook

logger = logging.getLogger(__name__)


SHORT_WAIT = .2  # S (200ms)
#
# The purpose of this class is to map the idea of a garage door to the pinouts on
# the raspberrypi. It provides methods to control the garage door and also provides
# and event hook to notify you of the state change. It also doesn't maintain any
# state internally but rather relies directly on reading the pin.
#
#
# There are several ways of getting GPIO input into your program. The first and simplest
#  way is to check the input value at a point in time. This is known as 'polling' and
# can potentially miss an input if your program reads the value at the wrong time.
# Polling is performed in loops and can potentially be processor intensive. The other
# way of responding to a GPIO input is using 'interrupts' (edge detection).
#
#
# An edge is the change in state of an electrical signal from LOW to HIGH (rising edge)
# or from HIGH to LOW (falling edge). Quite often, we are more concerned by a change in
# state of an input than it's value. This change in state is an event.
#


class GarageDoor(object):

    def __init__(self, config):
        # config
        self.relay_pin = config['relay_pin']
        self.state_pin = config['state_pin']
        self.id = config['id']
        self.name = config['name']
        # state_pin_closed_value = normally_closed = 0
        self.state_pin_closed_value = config.get('state_pin_closed_value', 0)
        self.time_to_close = config.get('approx_time_to_close', 10)
        self.time_to_open = config.get('approx_time_to_open', 10)
        self.invert_relay = bool(config.get('invert_relay'))

        # Setup
        self._state = None
        self.onStateChange = EventHook()

        try:
            gpio.setwarnings(False)
            # tell the GPIO module that we want to use
            # the chip's pin numbering scheme
            gpio.setmode(gpio.BCM)
            # Set relay pin to output
            gpio.setup(self.relay_pin, gpio.OUT)
            # Set state pin to input
            gpio.setup(self.state_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
            # add a change listener to the state pin
            # tell the GPIO library to look out for an
            # event on state_pin and deal with it by calling
            # the stateChanged function
            # The event_detected() function is designed to be used in a loop with
            # other things, but unlike polling it is not going to miss the change
            # in state of an input while the CPU is busy working on other things.
            gpio.add_event_detect(self.state_pin, gpio.BOTH,
                                  callback=self.stateChanged, bouncetime=300)

            # Set default relay state to true (on)
            gpio.output(self.relay_pin, self.invert_relay)
        except:
            logger.error("problem setting pins")
            gpio.cleanup()
            sys.exit(1)

    # Release rpi resources
    def __del__(self):
        gpio.cleanup()

    # These methods all just mimick the button press, they dont differ other than that
    # but for api sake I'll create three methods. Also later we may want to react to state
    # changes or do things differently depending on the intended action

    def open(self):
        if self.state == 'close':
            self.__press()

    def close(self):
        if self.state == 'open':
            self.__press()

    def stop(self):
        self.__press()

    # State is a getter,read only property that actually gets its value from the pin
    @property
    def state(self):
        # Read the mode from the config. Then compare the mode to the current state. IE.
        # If the circuit is normally closed and the state is 1 then the circuit is closed.
        # and vice versa for normally open
        try:
            current_state = gpio.input(self.state_pin)
            if current_state == self.state_pin_closed_value:
                return 'close'
            else:
                return 'open'
        except:
            logger.error("problem reading sensor")
            gpio.cleanup()
            sys.exit(1)

    # Mimick a button press by switching the gpio pin on and off quickly: triggerRelay
    def __press(self):
        try:
            gpio.output(self.relay_pin, not self.invert_relay)
            time.sleep(SHORT_WAIT)
            gpio.output(self.relay_pin, self.invert_relay)
        except:
            logger.error("problem triggering Relay")
            gpio.cleanup()
            sys.exit(1)

    # Provide an event for when the state pin changes
    def stateChanged(self, channel):
        try:
            if channel == self.state_pin:
                # Had some issues getting an accurate value so we are going to wait for a short timeout
                # after a statechange and then grab the state
                time.sleep(SHORT_WAIT)
                self.onStateChange.fire(self.state)
        except:
            logger.error("problem getting state change")
            gpio.cleanup()
            sys.exit(1)
