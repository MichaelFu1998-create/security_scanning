def print_error(message, wrap=True):
    """Print error message to stderr, using ANSI-colors.

    :param message: Message to print
    :param wrap:
        Wrap message into ``ERROR: <message>. Exit...`` template. By default:
        True
    """
    if wrap:
        message = 'ERROR: {0}. Exit...'.format(message.rstrip('.'))

    colorizer = (_color_wrap(colorama.Fore.RED)
                 if colorama
                 else lambda message: message)
    return print(colorizer(message), file=sys.stderr)