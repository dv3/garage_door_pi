import logging
from garage_door import GarageDoor

logger = logging.getLogger(__name__)


# Execute the specified command for a door
def execute_command(door, command):
    doorName = door.name
    logger.info("Executing command %s for door %s", command, doorName)
    if command == "OPEN" and door.state == 'closed':
        door.open()
    elif command == "CLOSE" and door.state == 'open':
        door.close()
    elif command == "STOP":
        door.stop()
    else:
        logger.info("Invalid command: %s", command)
