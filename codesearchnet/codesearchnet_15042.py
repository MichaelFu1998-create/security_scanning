def info(msg):
    """Emit a normal message."""
    _flush()
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()