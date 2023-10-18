def initFilter(input, filterInfo = None):
  """ Initializes internal filter variables for further processing.
  Returns a tuple (function to call,parameters for the filter call)

  The filterInfo is a dict. Here is an example structure:
    {fieldName: {'min': x,
                 'max': y,
                 'type': 'category', # or 'number'
                 'acceptValues': ['foo', 'bar'],
                 }
    }

  This returns the following:
    (filterFunc, ((fieldIdx, fieldFilterFunc, filterDict),
                  ...)

  Where fieldIdx is the index of the field within each record
        fieldFilterFunc returns True if the value is "OK" (within min, max or
           part of acceptValues)
        fieldDict is a dict containing 'type', 'min', max', 'acceptValues'
  """

  if filterInfo is None:
    return None

  # Build an array of index/func to call on record[index]
  filterList = []
  for i, fieldName in enumerate(input.getFieldNames()):
    fieldFilter = filterInfo.get(fieldName, None)
    if fieldFilter == None:
      continue

    var = dict()
    var['acceptValues'] = None
    min = fieldFilter.get('min', None)
    max = fieldFilter.get('max', None)
    var['min'] = min
    var['max'] = max


    if fieldFilter['type'] == 'category':
      var['acceptValues'] = fieldFilter['acceptValues']
      fp = lambda x: (x['value'] != SENTINEL_VALUE_FOR_MISSING_DATA and \
                      x['value'] in x['acceptValues'])

    elif fieldFilter['type'] == 'number':

      if min != None and max != None:
        fp = lambda x: (x['value'] != SENTINEL_VALUE_FOR_MISSING_DATA and \
                        x['value'] >= x['min'] and x['value'] <= x['max'])
      elif min != None:
        fp = lambda x: (x['value'] != SENTINEL_VALUE_FOR_MISSING_DATA and \
                        x['value'] >= x['min'])
      else:
        fp = lambda x: (x['value'] != SENTINEL_VALUE_FOR_MISSING_DATA and \
                        x['value'] <= x['max'])

    filterList.append((i, fp, var))

  return (_filterRecord, filterList)