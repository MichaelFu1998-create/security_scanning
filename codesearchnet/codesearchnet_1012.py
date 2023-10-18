def getBool(cls, prop):
    """ Retrieve the requested property and return it as a bool. If property
    does not exist, then KeyError will be raised. If the property value is
    neither 0 nor 1, then ValueError will be raised

    :param prop: (string) name of the property
    :raises: KeyError, ValueError
    :returns: (bool) property value
    """

    value = cls.getInt(prop)

    if value not in (0, 1):
      raise ValueError("Expected 0 or 1, but got %r in config property %s" % (
        value, prop))

    return bool(value)