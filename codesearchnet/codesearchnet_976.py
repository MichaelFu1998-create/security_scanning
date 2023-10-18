def _handleJAVAParameters(options):
  """ Handle legacy options (TEMPORARY) """

  # Find the correct InferenceType for the Model
  if 'inferenceType' not in options:
    prediction = options.get('prediction', {InferenceType.TemporalNextStep:
                                              {'optimize':True}})
    inferenceType = None
    for infType, value in prediction.iteritems():
      if value['optimize']:
        inferenceType = infType
        break

    if inferenceType == 'temporal':
      inferenceType = InferenceType.TemporalNextStep
    if inferenceType != InferenceType.TemporalNextStep:
      raise _ExpGeneratorException("Unsupported inference type %s"  % \
                                    (inferenceType))
    options['inferenceType'] = inferenceType

  # Find the best value for the predicted field
  if 'predictionField' in options:
    if 'inferenceArgs' not in options:
      options['inferenceArgs'] = {'predictedField': options['predictionField']}
    elif 'predictedField' not in options['inferenceArgs']:
      options['inferenceArgs']['predictedField'] = options['predictionField']