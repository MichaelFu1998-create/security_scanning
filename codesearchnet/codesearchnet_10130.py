def _cached_path_needs_update(ca_path, cache_length):
    """
    Checks to see if a cache file needs to be refreshed

    :param ca_path:
        A unicode string of the path to the cache file

    :param cache_length:
        An integer representing the number of hours the cache is valid for

    :return:
        A boolean - True if the cache needs to be updated, False if the file
        is up-to-date
    """

    exists = os.path.exists(ca_path)
    if not exists:
        return True

    stats = os.stat(ca_path)

    if stats.st_mtime < time.time() - cache_length * 60 * 60:
        return True

    if stats.st_size == 0:
        return True

    return False