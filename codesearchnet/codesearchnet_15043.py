def warning(msg):
    """Emit a warning message."""
    _flush()
    sys.stderr.write("\033[1;7;33;40mWARNING: {}\033[0m\n".format(msg))
    sys.stderr.flush()