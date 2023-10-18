def get_cache_key(user_or_username, size, prefix):
    """
    Returns a cache key consisten of a username and image size.
    """
    if isinstance(user_or_username, get_user_model()):
        user_or_username = user_or_username.username
    return '%s_%s_%s' % (prefix, user_or_username, size)