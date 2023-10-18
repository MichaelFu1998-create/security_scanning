def _generateEncoderStringsV1(includedFields):
  """ Generate and return the following encoder related substitution variables:

  encoderSpecsStr:
    For the base description file, this string defines the default
    encoding dicts for each encoder. For example:
         '__gym_encoder' : {   'fieldname': 'gym',
          'n': 13,
          'name': 'gym',
          'type': 'SDRCategoryEncoder',
          'w': 7},
        '__address_encoder' : {   'fieldname': 'address',
          'n': 13,
          'name': 'address',
          'type': 'SDRCategoryEncoder',
          'w': 7}

  encoderSchemaStr:
    For the base description file, this is a list containing a
    DeferredDictLookup entry for each encoder. For example:
        [DeferredDictLookup('__gym_encoder'),
         DeferredDictLookup('__address_encoder'),
         DeferredDictLookup('__timestamp_timeOfDay_encoder'),
         DeferredDictLookup('__timestamp_dayOfWeek_encoder'),
         DeferredDictLookup('__consumption_encoder')],

  permEncoderChoicesStr:
    For the permutations file, this defines the possible
    encoder dicts for each encoder. For example:
        '__timestamp_dayOfWeek_encoder': [
                     None,
                     {'fieldname':'timestamp',
                      'name': 'timestamp_timeOfDay',
                      'type':'DateEncoder'
                      'dayOfWeek': (7,1)
                      },
                     {'fieldname':'timestamp',
                      'name': 'timestamp_timeOfDay',
                      'type':'DateEncoder'
                      'dayOfWeek': (7,3)
                      },
                  ],

        '__field_consumption_encoder': [
                    None,
                    {'fieldname':'consumption',
                     'name': 'consumption',
                     'type':'AdaptiveScalarEncoder',
                     'n': 13,
                     'w': 7,
                      }
                   ]



  Parameters:
  --------------------------------------------------
  includedFields:  item from the 'includedFields' section of the
                    description JSON object. This is a list of dicts, each
                    dict defining the field name, type, and optional min
                    and max values.

  retval:  (encoderSpecsStr, encoderSchemaStr permEncoderChoicesStr)


  """

  # ------------------------------------------------------------------------
  # First accumulate the possible choices for each encoder
  encoderChoicesList = []
  for fieldInfo in includedFields:

    fieldName = fieldInfo['fieldName']

    # Get the list of encoder choices for this field
    (choicesList, aggFunction) = _generateEncoderChoicesV1(fieldInfo)
    encoderChoicesList.extend(choicesList)


  # ------------------------------------------------------------------------
  # Generate the string containing the encoder specs and encoder schema. See
  #  the function comments for an example of the encoderSpecsStr and
  #  encoderSchemaStr
  #
  encoderSpecsList = []
  for encoderChoices in encoderChoicesList:
    # Use the last choice as the default in the base file because the 1st is
    # often None
    encoder = encoderChoices[-1]

    # Check for bad characters
    for c in _ILLEGAL_FIELDNAME_CHARACTERS:
      if encoder['name'].find(c) >= 0:
        raise _ExpGeneratorException("Illegal character in field: %r (%r)" % (
          c, encoder['name']))

    encoderSpecsList.append("%s: \n%s%s" % (
        _quoteAndEscape(encoder['name']),
        2*_ONE_INDENT,
        pprint.pformat(encoder, indent=2*_INDENT_STEP)))

  encoderSpecsStr = ',\n  '.join(encoderSpecsList)


  # ------------------------------------------------------------------------
  # Generate the string containing the permutation encoder choices. See the
  #  function comments above for an example of the permEncoderChoicesStr

  permEncoderChoicesList = []
  for encoderChoices in encoderChoicesList:
    permEncoderChoicesList.append("%s: %s," % (
        _quoteAndEscape(encoderChoices[-1]['name']),
        pprint.pformat(encoderChoices, indent=2*_INDENT_STEP)))
  permEncoderChoicesStr = '\n'.join(permEncoderChoicesList)
  permEncoderChoicesStr = _indentLines(permEncoderChoicesStr, 1,
                                       indentFirstLine=False)

  # Return results
  return (encoderSpecsStr, permEncoderChoicesStr)