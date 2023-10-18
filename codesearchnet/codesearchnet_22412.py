def parse_int(s):
    """ Parse a string as an integer.
        Exit with a message on failure.
    """
    try:
        val = int(s)
    except ValueError:
        print_err('\nInvalid integer: {}'.format(s))
        sys.exit(1)
    return val