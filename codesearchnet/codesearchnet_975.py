def _generateEncoderStringsV2(includedFields, options):
  """ Generate and return the following encoder related substitution variables:

  encoderSpecsStr:
    For the base description file, this string defines the default
    encoding dicts for each encoder. For example:

         __gym_encoder = {   'fieldname': 'gym',
          'n': 13,
          'name': 'gym',
          'type': 'SDRCategoryEncoder',
          'w': 7},
        __address_encoder = {   'fieldname': 'address',
          'n': 13,
          'name': 'address',
          'type': 'SDRCategoryEncoder',
          'w': 7}


  permEncoderChoicesStr:
    For the permutations file, this defines the possible
    encoder dicts for each encoder. For example:

        '__gym_encoder' : PermuteEncoder('gym', 'SDRCategoryEncoder', w=7,
            n=100),

        '__address_encoder' : PermuteEncoder('address', 'SDRCategoryEncoder',
              w=7, n=100),

        '__timestamp_dayOfWeek_encoder' : PermuteEncoder('timestamp',
            'DateEncoder.timeOfDay', w=7, radius=PermuteChoices([1, 8])),

        '__consumption_encoder': PermuteEncoder('consumption', 'AdaptiveScalarEncoder',
            w=7, n=PermuteInt(13, 500, 20), minval=0,
            maxval=PermuteInt(100, 300, 25)),



  Parameters:
  --------------------------------------------------
  includedFields:  item from the 'includedFields' section of the
                    description JSON object. This is a list of dicts, each
                    dict defining the field name, type, and optional min
                    and max values.

  retval:  (encoderSpecsStr permEncoderChoicesStr)


  """

  width = 21
  encoderDictsList = []


  # If this is a NontemporalClassification experiment, then the
  #  the "predicted" field (the classification value) should be marked to ONLY
  #  go to the classifier
  if options['inferenceType'] in ["NontemporalClassification",
                                  "NontemporalMultiStep",
                                  "TemporalMultiStep",
                                  "MultiStep"]:
    classifierOnlyField = options['inferenceArgs']['predictedField']
  else:
    classifierOnlyField = None


  # ==========================================================================
  # For each field, generate the default encoding dict and PermuteEncoder
  #  constructor arguments
  for fieldInfo in includedFields:

    fieldName = fieldInfo['fieldName']
    fieldType = fieldInfo['fieldType']

    # ---------
    # Scalar?
    if fieldType in ['float', 'int']:
      # n=100 is reasonably hardcoded value for n when used by description.py
      # The swarming will use PermuteEncoder below, where n is variable and
      # depends on w
      runDelta = fieldInfo.get("runDelta", False)
      if runDelta or "space" in fieldInfo:
        encoderDict = dict(type='ScalarSpaceEncoder', name=fieldName,
                            fieldname=fieldName, n=100, w=width, clipInput=True)
        if runDelta:
          encoderDict["runDelta"] = True
      else:
        encoderDict = dict(type='AdaptiveScalarEncoder', name=fieldName,
                            fieldname=fieldName, n=100, w=width, clipInput=True)

      if 'minValue' in fieldInfo:
        encoderDict['minval'] = fieldInfo['minValue']
      if 'maxValue' in fieldInfo:
        encoderDict['maxval'] = fieldInfo['maxValue']

      # If both min and max were specified, use a non-adaptive encoder
      if ('minValue' in fieldInfo and 'maxValue' in fieldInfo) \
            and (encoderDict['type'] == 'AdaptiveScalarEncoder'):
        encoderDict['type'] = 'ScalarEncoder'

      # Defaults may have been over-ridden by specifying an encoder type
      if 'encoderType' in fieldInfo:
        encoderDict['type'] = fieldInfo['encoderType']

      if 'space' in fieldInfo:
        encoderDict['space'] = fieldInfo['space']
      encoderDictsList.append(encoderDict)



    # ---------
    # String?
    elif fieldType == 'string':
      encoderDict = dict(type='SDRCategoryEncoder', name=fieldName,
                     fieldname=fieldName, n=100+width, w=width)
      if 'encoderType' in fieldInfo:
        encoderDict['type'] = fieldInfo['encoderType']

      encoderDictsList.append(encoderDict)



    # ---------
    # Datetime?
    elif fieldType == 'datetime':

      # First, the time of day representation
      encoderDict = dict(type='DateEncoder', name='%s_timeOfDay' % (fieldName),
                     fieldname=fieldName, timeOfDay=(width, 1))
      if 'encoderType' in fieldInfo:
        encoderDict['type'] = fieldInfo['encoderType']
      encoderDictsList.append(encoderDict)


      # Now, the day of week representation
      encoderDict = dict(type='DateEncoder', name='%s_dayOfWeek' % (fieldName),
                     fieldname=fieldName, dayOfWeek=(width, 1))
      if 'encoderType' in fieldInfo:
        encoderDict['type'] = fieldInfo['encoderType']
      encoderDictsList.append(encoderDict)


      # Now, the day of week representation
      encoderDict = dict(type='DateEncoder', name='%s_weekend' % (fieldName),
                     fieldname=fieldName, weekend=(width))
      if 'encoderType' in fieldInfo:
        encoderDict['type'] = fieldInfo['encoderType']
      encoderDictsList.append(encoderDict)




    else:
      raise RuntimeError("Unsupported field type '%s'" % (fieldType))


    # -----------------------------------------------------------------------
    # If this was the predicted field, insert another encoder that sends it
    # to the classifier only
    if fieldName == classifierOnlyField:
      clEncoderDict = dict(encoderDict)
      clEncoderDict['classifierOnly'] = True
      clEncoderDict['name'] = '_classifierInput'
      encoderDictsList.append(clEncoderDict)

      # If the predicted field needs to be excluded, take it out of the encoder
      #  lists
      if options["inferenceArgs"]["inputPredictedField"] == "no":
        encoderDictsList.remove(encoderDict)

  # Remove any encoders not in fixedFields
  if options.get('fixedFields') is not None:
    tempList=[]
    for encoderDict in encoderDictsList:
      if encoderDict['name'] in options['fixedFields']:
        tempList.append(encoderDict)
    encoderDictsList = tempList

  # ==========================================================================
  # Now generate the encoderSpecsStr and permEncoderChoicesStr strings from
  #  encoderDictsList and constructorStringList

  encoderSpecsList = []
  permEncoderChoicesList = []
  for encoderDict in encoderDictsList:

    if encoderDict['name'].find('\\') >= 0:
      raise _ExpGeneratorException("Illegal character in field: '\\'")

    # Check for bad characters
    for c in _ILLEGAL_FIELDNAME_CHARACTERS:
      if encoderDict['name'].find(c) >= 0:
        raise _ExpGeneratorException("Illegal character %s in field %r"  %(c, encoderDict['name']))

    constructorStr = _generatePermEncoderStr(options, encoderDict)

    encoderKey = _quoteAndEscape(encoderDict['name'])
    encoderSpecsList.append("%s: %s%s" % (
        encoderKey,
        2*_ONE_INDENT,
        pprint.pformat(encoderDict, indent=2*_INDENT_STEP)))


    # Each permEncoderChoicesStr is of the form:
    #  PermuteEncoder('gym', 'SDRCategoryEncoder',
    #          w=7, n=100),
    permEncoderChoicesList.append("%s: %s," % (encoderKey, constructorStr))


  # Join into strings
  encoderSpecsStr = ',\n  '.join(encoderSpecsList)

  permEncoderChoicesStr = '\n'.join(permEncoderChoicesList)
  permEncoderChoicesStr = _indentLines(permEncoderChoicesStr, 1,
                                       indentFirstLine=True)

  # Return results
  return (encoderSpecsStr, permEncoderChoicesStr)