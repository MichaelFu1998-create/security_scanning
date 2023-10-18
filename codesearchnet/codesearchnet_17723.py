def _translateCommands(commands):
    """Generate the binary strings for a comma seperated list of commands."""
    for command in commands.split(','):
        # each command results in 2 bytes of binary data
        result = [0, 0]
        device, command = command.strip().upper().split(None, 1)

        # translate the house code
        result[0] = houseCodes[device[0]]

        # translate the device number if there is one
        if len(device) > 1:
            deviceNumber = deviceNumbers[device[1:]]
            result[0] |= deviceNumber[0]
            result[1] = deviceNumber[1]

        # translate the command
        result[1] |= commandCodes[command]

        # convert 2 bytes to bit strings and yield them
        yield ' '.join(map(_strBinary, result))