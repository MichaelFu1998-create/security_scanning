def getString(cls, prop):
    """ Retrieve the requested property as a string. If property does not exist,
    then KeyError will be raised.

    :param prop: (string) name of the property
    :raises: KeyError
    :returns: (string) property value
    """
    if cls._properties is None:
      cls._readStdConfigFiles()

    # Allow configuration properties to be overridden via environment variables
    envValue = os.environ.get("%s%s" % (cls.envPropPrefix,
                                        prop.replace('.', '_')), None)
    if envValue is not None:
      return envValue

    return cls._properties[prop]