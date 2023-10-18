def _generateExtraMetricSpecs(options):
  """Generates the non-default metrics specified by the expGenerator params """
  _metricSpecSchema = {'properties': {}}

  results = []
  for metric in options['metrics']:

    for propertyName in _metricSpecSchema['properties'].keys():
      _getPropertyValue(_metricSpecSchema, propertyName, metric)


    specString, label = _generateMetricSpecString(
                                          field=metric['field'],
                                          metric=metric['metric'],
                                          params=metric['params'],
                                          inferenceElement=\
                                                    metric['inferenceElement'],
                                          returnLabel=True)
    if metric['logged']:
      options['loggedMetrics'].append(label)

    results.append(specString)

  return results