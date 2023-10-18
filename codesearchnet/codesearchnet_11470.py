def read_file(filepath):
    """
    Retrieves the contents of the specified file.

    This function performs simple caching so that the same file isn't read more
    than once per process.

    :param filepath: the file to read
    :type filepath: str
    :returns: str
    """

    with _FILE_CACHE_LOCK:
        if filepath not in _FILE_CACHE:
            _FILE_CACHE[filepath] = _read_file(filepath)
    return _FILE_CACHE[filepath]