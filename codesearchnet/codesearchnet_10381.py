def unlink_f(path):
    """Unlink path but do not complain if file does not exist."""
    try:
        os.unlink(path)
    except OSError as err:
        if err.errno != errno.ENOENT:
            raise