def _readConfigFile(cls, filename, path=None):
    """ Parse the given XML file and return a dict describing the file.

    Parameters:
    ----------------------------------------------------------------
    filename:  name of XML file to parse (no path)
    path:      path of the XML file. If None, then use the standard
                  configuration search path.
    retval:    returns a dict with each property as a key and a dict of all
               the property's attributes as value
    """

    outputProperties = dict()

    # Get the path to the config files.
    if path is None:
      filePath = cls.findConfigFile(filename)
    else:
      filePath = os.path.join(path, filename)

    # ------------------------------------------------------------------
    # Read in the config file
    try:
      if filePath is not None:
        try:
          # Use warn since console log level is set to warning
          _getLoggerBase().debug("Loading config file: %s", filePath)
          with open(filePath, 'r') as inp:
            contents = inp.read()
        except Exception:
          raise RuntimeError("Expected configuration file at %s" % filePath)
      else:
        # If the file was not found in the normal search paths, which includes
        # checking the NTA_CONF_PATH, we'll try loading it from pkg_resources.
        try:
          contents = resource_string("nupic.support", filename)
        except Exception as resourceException:
          # We expect these to be read, and if they don't exist we'll just use
          # an empty configuration string.
          if filename in [USER_CONFIG, CUSTOM_CONFIG]:
            contents = '<configuration/>'
          else:
            raise resourceException

      elements = ElementTree.XML(contents)

      if elements.tag != 'configuration':
        raise RuntimeError("Expected top-level element to be 'configuration' "
                           "but got '%s'" % (elements.tag))

      # ------------------------------------------------------------------
      # Add in each property found
      propertyElements = elements.findall('./property')

      for propertyItem in propertyElements:

        propInfo = dict()

        # Parse this property element
        propertyAttributes = list(propertyItem)
        for propertyAttribute in propertyAttributes:
          propInfo[propertyAttribute.tag] = propertyAttribute.text

        # Get the name
        name = propInfo.get('name', None)

        # value is allowed to be empty string
        if 'value' in propInfo and propInfo['value'] is None:
          value = ''
        else:
          value = propInfo.get('value', None)

          if value is None:
            if 'novalue' in propInfo:
              # Placeholder "novalue" properties are intended to be overridden
              # via dynamic configuration or another configuration layer.
              continue
            else:
              raise RuntimeError("Missing 'value' element within the property "
                                 "element: => %s " % (str(propInfo)))

        # The value is allowed to contain substitution tags of the form
        # ${env.VARNAME}, which should be substituted with the corresponding
        # environment variable values
        restOfValue = value
        value = ''
        while True:
          # Find the beginning of substitution tag
          pos = restOfValue.find('${env.')
          if pos == -1:
            # No more environment variable substitutions
            value += restOfValue
            break

          # Append prefix to value accumulator
          value += restOfValue[0:pos]

          # Find the end of current substitution tag
          varTailPos = restOfValue.find('}', pos)
          if varTailPos == -1:
            raise RuntimeError(
              "Trailing environment variable tag delimiter '}'"
              " not found in %r" % (restOfValue))

          # Extract environment variable name from tag
          varname = restOfValue[pos + 6:varTailPos]
          if varname not in os.environ:
            raise RuntimeError("Attempting to use the value of the environment"
                               " variable %r, which is not defined" % (
                               varname))
          envVarValue = os.environ[varname]

          value += envVarValue

          restOfValue = restOfValue[varTailPos + 1:]

        # Check for errors
        if name is None:
          raise RuntimeError(
            "Missing 'name' element within following property "
            "element:\n => %s " % (str(propInfo)))

        propInfo['value'] = value
        outputProperties[name] = propInfo

      return outputProperties
    except Exception:
      _getLoggerBase().exception("Error while parsing configuration file: %s.",
                             filePath)
      raise