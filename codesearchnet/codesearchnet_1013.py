def set(cls, prop, value):
    """ Set the value of the given configuration property.

    :param prop: (string) name of the property
    :param value: (object) value to set
    """

    if cls._properties is None:
      cls._readStdConfigFiles()

    cls._properties[prop] = str(value)