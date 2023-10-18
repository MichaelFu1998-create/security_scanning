def banner(msg):
    """Emit a banner just like Invoke's `run(…, echo=True)`."""
    if ECHO:
        _flush()
        sys.stderr.write("\033[1;7;32;40m{}\033[0m\n".format(msg))
        sys.stderr.flush()