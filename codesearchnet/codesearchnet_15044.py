def error(msg):
    """Emit an error message to stderr."""
    _flush()
    sys.stderr.write("\033[1;37;41mERROR: {}\033[0m\n".format(msg))
    sys.stderr.flush()