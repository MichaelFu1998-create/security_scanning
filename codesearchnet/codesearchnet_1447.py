def getCustomDict(cls):
    """ Returns a dict of all temporary values in custom configuration file

    """
    if not os.path.exists(cls.getPath()):
      return dict()

    properties = Configuration._readConfigFile(os.path.basename(
      cls.getPath()), os.path.dirname(cls.getPath()))

    values = dict()
    for propName in properties:
      if 'value' in properties[propName]:
        values[propName] = properties[propName]['value']

    return values