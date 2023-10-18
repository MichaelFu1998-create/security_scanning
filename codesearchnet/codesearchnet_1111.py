def _getStreamDef(self, modelDescription):
    """
    Generate stream definition based on
    """
    #--------------------------------------------------------------------------
    # Generate the string containing the aggregation settings.
    aggregationPeriod = {
        'days': 0,
        'hours': 0,
        'microseconds': 0,
        'milliseconds': 0,
        'minutes': 0,
        'months': 0,
        'seconds': 0,
        'weeks': 0,
        'years': 0,
    }

    # Honor any overrides provided in the stream definition
    aggFunctionsDict = {}
    if 'aggregation' in modelDescription['streamDef']:
      for key in aggregationPeriod.keys():
        if key in modelDescription['streamDef']['aggregation']:
          aggregationPeriod[key] = modelDescription['streamDef']['aggregation'][key]
      if 'fields' in modelDescription['streamDef']['aggregation']:
        for (fieldName, func) in modelDescription['streamDef']['aggregation']['fields']:
          aggFunctionsDict[fieldName] = str(func)

    # Do we have any aggregation at all?
    hasAggregation = False
    for v in aggregationPeriod.values():
      if v != 0:
        hasAggregation = True
        break

    # Convert the aggFunctionsDict to a list
    aggFunctionList = aggFunctionsDict.items()
    aggregationInfo = dict(aggregationPeriod)
    aggregationInfo['fields'] = aggFunctionList

    streamDef = copy.deepcopy(modelDescription['streamDef'])
    streamDef['aggregation'] = copy.deepcopy(aggregationInfo)
    return streamDef