def sendCommands(comPort, commands):
    """Send X10 commands using the FireCracker on comPort

    comPort should be the name of a serial port on the host platform. On
    Windows, for example, 'com1'.

    commands should be a string consisting of X10 commands separated by
    commas. For example. 'A1 On, A Dim, A Dim, A Dim, A Lamps Off'. The
    letter is a house code (A-P) and the number is the device number (1-16).
    Possible commands for a house code / device number combination are
    'On' and 'Off'. The commands 'Bright' and 'Dim' should be used with a
    house code alone after sending an On command to a specific device. The
    'All On', 'All Off', 'Lamps On', and 'Lamps Off' commands should also
    be used with a house code alone.

    # Turn on module A1
    >>> sendCommands('com1', 'A1 On')

    # Turn all modules with house code A off
    >>> sendCommands('com1', 'A All Off')

    # Turn all lamp modules with house code B on
    >>> sendCommands('com1', 'B Lamps On')

    # Turn on module A1 and dim it 3 steps, then brighten it 1 step
    >>> sendCommands('com1', 'A1 On, A Dim, A Dim, A Dim, A Bright')
    """
    mutex.acquire()
    try:
        try:
            port = serial.Serial(port=comPort)
            header = '11010101 10101010'
            footer = '10101101'
            for command in _translateCommands(commands):
                _sendBinaryData(port, header + command + footer)
        except serial.SerialException:
            print('Unable to open serial port %s' % comPort)
            print('')
            raise
    finally:
        mutex.release()