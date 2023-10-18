def dict(cls):
    """ Return a dict containing all of the configuration properties

    :returns: (dict) containing all configuration properties.
    """

    if cls._properties is None:
      cls._readStdConfigFiles()

    # Make a copy so we can update any current values obtained from environment
    #  variables
    result = dict(cls._properties)
    keys = os.environ.keys()
    replaceKeys = filter(lambda x: x.startswith(cls.envPropPrefix),
                         keys)
    for envKey in replaceKeys:
      key = envKey[len(cls.envPropPrefix):]
      key = key.replace('_', '.')
      result[key] = os.environ[envKey]

    return result