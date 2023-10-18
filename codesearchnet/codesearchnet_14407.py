def env(key, default):
    """
    Helper to try to get a setting from the environment, or pyconfig, or
    finally use a provided default.

    """
    value = os.environ.get(key, None)
    if value is not None:
        log.info('    %s = %r', key.lower().replace('_', '.'), value)
        return value

    key = key.lower().replace('_', '.')
    value = get(key)
    if value is not None:
        return value

    return default