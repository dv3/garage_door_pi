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
