def writable_path(path):
    """Test whether a path can be written to.
    """
    if os.path.exists(path):
        return os.access(path, os.W_OK)
    try:
        with open(path, 'w'):
            pass
    except (OSError, IOError):
        return False
    else:
        os.remove(path)
        return True