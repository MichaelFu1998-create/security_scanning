def resetCustomConfig(cls):
    """ Clear all custom configuration settings and delete the persistent
    custom configuration store.
    """
    _getLogger().info("Resetting all custom configuration properties; "
                      "caller=%r", traceback.format_stack())

    # Clear the in-memory settings cache, forcing reload upon subsequent "get"
    # request.
    super(Configuration, cls).clear()

    # Delete the persistent custom configuration store and reset in-memory
    # custom configuration info
    _CustomConfigurationFileWrapper.clear(persistent=True)