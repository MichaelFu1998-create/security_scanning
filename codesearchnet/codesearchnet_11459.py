def purge_config_cache(location=None):
    """
    Clears out the cache of TidyPy configurations that were retrieved from
    outside the normal locations.
    """

    cache_path = get_cache_path(location)

    if location:
        os.remove(cache_path)
    else:
        shutil.rmtree(cache_path)