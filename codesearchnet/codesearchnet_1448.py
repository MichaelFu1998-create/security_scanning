def edit(cls, properties):
    """ Edits the XML configuration file with the parameters specified by
    properties

    Parameters:
    ----------------------------------------------------------------
    properties: dict of settings to be applied to the custom configuration store
                 (key is property name, value is value)
    """
    copyOfProperties = copy(properties)

    configFilePath = cls.getPath()

    try:
      with open(configFilePath, 'r') as fp:
        contents = fp.read()
    except IOError, e:
      if e.errno != errno.ENOENT:
        _getLogger().exception("Error %s reading custom configuration store "
                               "from %s, while editing properties %s.",
                               e.errno, configFilePath, properties)
        raise
      contents = '<configuration/>'

    try:
      elements = ElementTree.XML(contents)
      ElementTree.tostring(elements)
    except Exception, e:
      # Raising error as RuntimeError with custom message since ElementTree
      # exceptions aren't clear.
      msg = "File contents of custom configuration is corrupt.  File " \
            "location: %s; Contents: '%s'. Original Error (%s): %s." % \
            (configFilePath, contents, type(e), e)
      _getLogger().exception(msg)
      raise RuntimeError(msg), None, sys.exc_info()[2]

    if elements.tag != 'configuration':
      e = "Expected top-level element to be 'configuration' but got '%s'" % \
          (elements.tag)
      _getLogger().error(e)
      raise RuntimeError(e)

    # Apply new properties to matching settings in the custom config store;
    # pop matching properties from our copy of the properties dict
    for propertyItem in elements.findall('./property'):
      propInfo = dict((attr.tag, attr.text) for attr in propertyItem)
      name = propInfo['name']
      if name in copyOfProperties:
        foundValues = propertyItem.findall('./value')
        if len(foundValues) > 0:
          foundValues[0].text = str(copyOfProperties.pop(name))
          if not copyOfProperties:
            break
        else:
          e = "Property %s missing value tag." % (name,)
          _getLogger().error(e)
          raise RuntimeError(e)

    # Add unmatched remaining properties to custom config store
    for propertyName, value in copyOfProperties.iteritems():
      newProp = ElementTree.Element('property')
      nameTag = ElementTree.Element('name')
      nameTag.text = propertyName
      newProp.append(nameTag)

      valueTag = ElementTree.Element('value')
      valueTag.text = str(value)
      newProp.append(valueTag)

      elements.append(newProp)

    try:
      makeDirectoryFromAbsolutePath(os.path.dirname(configFilePath))
      with open(configFilePath, 'w') as fp:
        fp.write(ElementTree.tostring(elements))
    except Exception, e:
      _getLogger().exception("Error while saving custom configuration "
                             "properties %s in %s.", properties,
                             configFilePath)
      raise