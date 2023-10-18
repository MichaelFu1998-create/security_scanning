def _generateInferenceArgs(options, tokenReplacements):
  """ Generates the token substitutions related to the predicted field
  and the supplemental arguments for prediction
  """
  inferenceType = options['inferenceType']
  optionInferenceArgs = options.get('inferenceArgs', None)
  resultInferenceArgs = {}
  predictedField = _getPredictedField(options)[0]

  if inferenceType in (InferenceType.TemporalNextStep,
                       InferenceType.TemporalAnomaly):
    assert predictedField,  "Inference Type '%s' needs a predictedField "\
                            "specified in the inferenceArgs dictionary"\
                            % inferenceType

  if optionInferenceArgs:
    # If we will be using a dynamically created predictionSteps, plug in that
    #  variable name in place of the constant scalar value
    if options['dynamicPredictionSteps']:
      altOptionInferenceArgs = copy.deepcopy(optionInferenceArgs)
      altOptionInferenceArgs['predictionSteps'] = '$REPLACE_ME'
      resultInferenceArgs = pprint.pformat(altOptionInferenceArgs)
      resultInferenceArgs = resultInferenceArgs.replace("'$REPLACE_ME'",
                                                        '[predictionSteps]')
    else:
      resultInferenceArgs = pprint.pformat(optionInferenceArgs)

  tokenReplacements['\$INFERENCE_ARGS'] = resultInferenceArgs

  tokenReplacements['\$PREDICTION_FIELD'] = predictedField