def _error(msg, *args):
    """
    Print an error message and exit.

    :param msg: A message to print
    :type msg: str

    """
    print(msg % args, file=sys.stderr)
    sys.exit(1)