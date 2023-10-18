def readConfigFile(cls, filename, path=None):
    """ Parse the given XML file and store all properties it describes.

    :param filename: (string) name of XML file to parse (no path)
    :param path: (string) path of the XML file. If None, then use the standard
                  configuration search path.
    """
    properties = cls._readConfigFile(filename, path)

    # Create properties dict if necessary
    if cls._properties is None:
      cls._properties = dict()

    for name in properties:
      if 'value' in properties[name]:
        cls._properties[name] = properties[name]['value']