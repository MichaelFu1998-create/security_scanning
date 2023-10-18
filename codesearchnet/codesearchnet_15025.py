def fail(message, exitcode=1):
    """Exit with error code and message."""
    sys.stderr.write('ERROR: {}\n'.format(message))
    sys.stderr.flush()
    sys.exit(exitcode)