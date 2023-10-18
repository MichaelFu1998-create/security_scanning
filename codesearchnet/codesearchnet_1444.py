def clear(cls):
    """ Clear all configuration properties from in-memory cache, but do NOT
    alter the custom configuration file. Used in unit-testing.
    """
    # Clear the in-memory settings cache, forcing reload upon subsequent "get"
    # request.
    super(Configuration, cls).clear()

    # Reset in-memory custom configuration info.
    _CustomConfigurationFileWrapper.clear(persistent=False)