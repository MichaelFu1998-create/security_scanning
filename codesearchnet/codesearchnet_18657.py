def select(options=None):
    """ pass in a list of options, promt the user to select one, and return the selected option or None """
    if not options:
        return None
    width = len(str(len(options)))
    for x,option in enumerate(options):
        sys.stdout.write('{:{width}}) {}\n'.format(x+1,option, width=width))

    sys.stdout.write('{:>{width}} '.format('#?', width=width+1))
    sys.stdout.flush()
    if sys.stdin.isatty():
        # regular prompt
        try:
            response = raw_input().strip()
        except (EOFError, KeyboardInterrupt):
            # handle ctrl-d, ctrl-c
            response = ''
    else:
        # try connecting to current tty, when using pipes
        sys.stdin = open("/dev/tty")
        try:
            response = ''
            while True:
                response += sys.stdin.read(1)
                if response.endswith('\n'):
                    break
        except (EOFError, KeyboardInterrupt):
            sys.stdout.flush()
            pass
    try:
        response = int(response) - 1
    except ValueError:
        return None
    if response < 0 or response >= len(options):
        return None
    return options[response]