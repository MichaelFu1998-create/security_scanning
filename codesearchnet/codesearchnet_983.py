def _getPredictedField(options):
  """ Gets the predicted field and it's datatype from the options dictionary

  Returns: (predictedFieldName, predictedFieldType)
  """
  if not options['inferenceArgs'] or \
      not options['inferenceArgs']['predictedField']:
    return None, None

  predictedField = options['inferenceArgs']['predictedField']
  predictedFieldInfo = None
  includedFields = options['includedFields']

  for info in includedFields:
    if info['fieldName'] == predictedField:
      predictedFieldInfo = info
      break

  if predictedFieldInfo is None:
    raise ValueError(
      "Predicted field '%s' does not exist in included fields." % predictedField
    )
  predictedFieldType = predictedFieldInfo['fieldType']

  return predictedField, predictedFieldType