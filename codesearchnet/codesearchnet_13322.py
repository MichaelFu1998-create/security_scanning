def set_stringprep_cache_size(size):
    """Modify stringprep cache size.

    :Parameters:
        - `size`: new cache size
    """
    # pylint: disable-msg=W0603
    global _stringprep_cache_size
    _stringprep_cache_size = size
    if len(Profile.cache_items) > size:
        remove = Profile.cache_items[:-size]
        for profile, key in remove:
            try:
                del profile.cache[key]
            except KeyError:
                pass
        Profile.cache_items = Profile.cache_items[-size:]