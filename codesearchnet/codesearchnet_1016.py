def findConfigFile(cls, filename):
    """ Search the configuration path (specified via the NTA_CONF_PATH
    environment variable) for the given filename. If found, return the complete
    path to the file.

    :param filename: (string) name of file to locate
    """

    paths = cls.getConfigPaths()
    for p in paths:
      testPath = os.path.join(p, filename)
      if os.path.isfile(testPath):
        return os.path.join(p, filename)