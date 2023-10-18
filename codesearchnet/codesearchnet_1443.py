def setCustomProperties(cls, properties):
    """ Set multiple custom properties and persist them to the custom
    configuration store.

    Parameters:
    ----------------------------------------------------------------
    properties: a dict of property name/value pairs to set
    """
    _getLogger().info("Setting custom configuration properties=%r; caller=%r",
                      properties, traceback.format_stack())

    _CustomConfigurationFileWrapper.edit(properties)

    for propertyName, value in properties.iteritems():
      cls.set(propertyName, value)