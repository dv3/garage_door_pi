import os
import binascii
import json
import re
from garage_door import GarageDoor


# Execute the specified command for a door
def execute_command(door, command):
    doorName = door.name
    print("Executing command %s for door %s", command, doorName)
    if command == "OPEN" and door.state == 'closed':
        door.open()
    elif command == "CLOSE" and door.state == 'open':
        door.close()
    elif command == "STOP":
        door.stop()
    else:
        print("Invalid command: %s", command)


class Controller(object):
    def __init__(self):

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        # try:
        #     client.loop_forever()
        # finally:
        #     client.disconnect()
        #     conn.close()
