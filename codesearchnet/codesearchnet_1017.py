def getConfigPaths(cls):
    """ Return the list of paths to search for configuration files.

    :returns: (list) of paths
    """
    configPaths = []
    if cls._configPaths is not None:
      return cls._configPaths

    else:
      if 'NTA_CONF_PATH' in os.environ:
        configVar = os.environ['NTA_CONF_PATH']
        # Return as a list of paths
        configPaths = configVar.split(os.pathsep)

      return configPaths