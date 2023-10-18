def main(argv=None):
    """Send X10 commands when module is used from the command line.

    This uses syntax similar to sendCommands, for example:

    x10.py com2 A1 On, A2 Off, B All Off
    """
    if len(argv):
        # join all the arguments together by spaces so that quotes
        # aren't required on the command line.
        commands = ' '.join(argv)

        # the comPort is everything leading up to the first space
        comPort, commands = commands.split(None, 1)

        sendCommands(comPort, commands)

    return 0