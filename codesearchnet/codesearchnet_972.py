def _generateEncoderChoicesV1(fieldInfo):
  """ Return a list of possible encoder parameter combinations for the given
  field and the default aggregation function to use. Each parameter combination
  is a dict defining the parameters for the encoder. Here is an example
  return value for the encoderChoicesList:

   [
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

  Parameters:
  --------------------------------------------------
  fieldInfo:      item from the 'includedFields' section of the
                    description JSON object

  retval:  (encoderChoicesList, aggFunction)
             encoderChoicesList: a list of encoder choice lists for this field.
               Most fields will generate just 1 encoder choice list.
               DateTime fields can generate 2 or more encoder choice lists,
                 one for dayOfWeek, one for timeOfDay, etc.
             aggFunction: name of aggregation function to use for this
                           field type

  """

  width = 7
  fieldName = fieldInfo['fieldName']
  fieldType = fieldInfo['fieldType']
  encoderChoicesList = []

  # Scalar?
  if fieldType in ['float', 'int']:
    aggFunction = 'mean'
    encoders = [None]
    for n in (13, 50, 150, 500):
      encoder = dict(type='ScalarSpaceEncoder', name=fieldName, fieldname=fieldName,
                     n=n, w=width, clipInput=True,space="absolute")
      if 'minValue' in fieldInfo:
        encoder['minval'] = fieldInfo['minValue']
      if 'maxValue' in fieldInfo:
        encoder['maxval'] = fieldInfo['maxValue']
      encoders.append(encoder)
    encoderChoicesList.append(encoders)

  # String?
  elif fieldType == 'string':
    aggFunction = 'first'
    encoders = [None]
    encoder = dict(type='SDRCategoryEncoder', name=fieldName,
                   fieldname=fieldName, n=100, w=width)
    encoders.append(encoder)
    encoderChoicesList.append(encoders)


  # Datetime?
  elif fieldType == 'datetime':
    aggFunction = 'first'

    # First, the time of day representation
    encoders = [None]
    for radius in (1, 8):
      encoder = dict(type='DateEncoder', name='%s_timeOfDay' % (fieldName),
                     fieldname=fieldName, timeOfDay=(width, radius))
      encoders.append(encoder)
    encoderChoicesList.append(encoders)

    # Now, the day of week representation
    encoders = [None]
    for radius in (1, 3):
      encoder = dict(type='DateEncoder', name='%s_dayOfWeek' % (fieldName),
                     fieldname=fieldName, dayOfWeek=(width, radius))
      encoders.append(encoder)
    encoderChoicesList.append(encoders)

  else:
    raise RuntimeError("Unsupported field type '%s'" % (fieldType))


  # Return results
  return (encoderChoicesList, aggFunction)