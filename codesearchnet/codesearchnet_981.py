def _generateMetricSpecs(options):
  """ Generates the Metrics for a given InferenceType

  Parameters:
  -------------------------------------------------------------------------
  options: ExpGenerator options
  retval: (metricsList, optimizeMetricLabel)
            metricsList: list of metric string names
            optimizeMetricLabel: Name of the metric which to optimize over

  """
  inferenceType = options['inferenceType']
  inferenceArgs = options['inferenceArgs']
  predictionSteps = inferenceArgs['predictionSteps']
  metricWindow = options['metricWindow']
  if metricWindow is None:
    metricWindow = int(Configuration.get("nupic.opf.metricWindow"))

  metricSpecStrings = []
  optimizeMetricLabel = ""

  # -----------------------------------------------------------------------
  # Generate the metrics specified by the expGenerator paramters
  metricSpecStrings.extend(_generateExtraMetricSpecs(options))

  # -----------------------------------------------------------------------

  optimizeMetricSpec = None
  # If using a dynamically computed prediction steps (i.e. when swarming
  #  over aggregation is requested), then we will plug in the variable
  #  predictionSteps in place of the statically provided predictionSteps
  #  from the JSON description.
  if options['dynamicPredictionSteps']:
    assert len(predictionSteps) == 1
    predictionSteps = ['$REPLACE_ME']

  # -----------------------------------------------------------------------
  # Metrics for temporal prediction
  if inferenceType in (InferenceType.TemporalNextStep,
                       InferenceType.TemporalAnomaly,
                       InferenceType.TemporalMultiStep,
                       InferenceType.NontemporalMultiStep,
                       InferenceType.NontemporalClassification,
                       'MultiStep'):

    predictedFieldName, predictedFieldType = _getPredictedField(options)
    isCategory = _isCategory(predictedFieldType)
    metricNames = ('avg_err',) if isCategory else ('aae', 'altMAPE')
    trivialErrorMetric = 'avg_err' if isCategory else 'altMAPE'
    oneGramErrorMetric = 'avg_err' if isCategory else 'altMAPE'
    movingAverageBaselineName = 'moving_mode' if isCategory else 'moving_mean'

    # Multi-step metrics
    for metricName in metricNames:
      metricSpec, metricLabel = \
        _generateMetricSpecString(field=predictedFieldName,
                 inferenceElement=InferenceElement.multiStepBestPredictions,
                 metric='multiStep',
                 params={'errorMetric': metricName,
                               'window':metricWindow,
                               'steps': predictionSteps},
                 returnLabel=True)
      metricSpecStrings.append(metricSpec)

    # If the custom error metric was specified, add that
    if options["customErrorMetric"] is not None :
      metricParams = dict(options["customErrorMetric"])
      metricParams['errorMetric'] = 'custom_error_metric'
      metricParams['steps'] = predictionSteps
      # If errorWindow is not specified, make it equal to the default window
      if not "errorWindow" in metricParams:
        metricParams["errorWindow"] = metricWindow
      metricSpec, metricLabel =_generateMetricSpecString(field=predictedFieldName,
                   inferenceElement=InferenceElement.multiStepPredictions,
                   metric="multiStep",
                   params=metricParams,
                   returnLabel=True)
      metricSpecStrings.append(metricSpec)

    # If this is the first specified step size, optimize for it. Be sure to
    #  escape special characters since this is a regular expression
    optimizeMetricSpec = metricSpec
    metricLabel = metricLabel.replace('[', '\\[')
    metricLabel = metricLabel.replace(']', '\\]')
    optimizeMetricLabel = metricLabel

    if options["customErrorMetric"] is not None :
      optimizeMetricLabel = ".*custom_error_metric.*"

    # Add in the trivial metrics
    if options["runBaselines"] \
          and inferenceType != InferenceType.NontemporalClassification:
      for steps in predictionSteps:
        metricSpecStrings.append(
          _generateMetricSpecString(field=predictedFieldName,
                                    inferenceElement=InferenceElement.prediction,
                                    metric="trivial",
                                    params={'window':metricWindow,
                                                  "errorMetric":trivialErrorMetric,
                                                  'steps': steps})
          )

        ##Add in the One-Gram baseline error metric
        #metricSpecStrings.append(
        #  _generateMetricSpecString(field=predictedFieldName,
        #                            inferenceElement=InferenceElement.encodings,
        #                            metric="two_gram",
        #                            params={'window':metricWindow,
        #                                          "errorMetric":oneGramErrorMetric,
        #                                          'predictionField':predictedFieldName,
        #                                          'steps': steps})
        #  )
        #
        #Include the baseline moving mean/mode metric
        if isCategory:
          metricSpecStrings.append(
            _generateMetricSpecString(field=predictedFieldName,
                                      inferenceElement=InferenceElement.prediction,
                                      metric=movingAverageBaselineName,
                                      params={'window':metricWindow
                                                    ,"errorMetric":"avg_err",
                                                    "mode_window":200,
                                                    "steps": steps})
            )
        else :
          metricSpecStrings.append(
            _generateMetricSpecString(field=predictedFieldName,
                                      inferenceElement=InferenceElement.prediction,
                                      metric=movingAverageBaselineName,
                                      params={'window':metricWindow
                                                    ,"errorMetric":"altMAPE",
                                                    "mean_window":200,
                                                    "steps": steps})
            )




  # -----------------------------------------------------------------------
  # Metrics for classification
  elif inferenceType in (InferenceType.TemporalClassification):

    metricName = 'avg_err'
    trivialErrorMetric = 'avg_err'
    oneGramErrorMetric = 'avg_err'
    movingAverageBaselineName = 'moving_mode'

    optimizeMetricSpec, optimizeMetricLabel = \
      _generateMetricSpecString(inferenceElement=InferenceElement.classification,
                               metric=metricName,
                               params={'window':metricWindow},
                               returnLabel=True)

    metricSpecStrings.append(optimizeMetricSpec)

    if options["runBaselines"]:
      # If temporal, generate the trivial predictor metric
      if inferenceType == InferenceType.TemporalClassification:
        metricSpecStrings.append(
          _generateMetricSpecString(inferenceElement=InferenceElement.classification,
                                    metric="trivial",
                                    params={'window':metricWindow,
                                                  "errorMetric":trivialErrorMetric})
          )
        metricSpecStrings.append(
          _generateMetricSpecString(inferenceElement=InferenceElement.classification,
                                    metric="two_gram",
                                    params={'window':metricWindow,
                                                  "errorMetric":oneGramErrorMetric})
          )
        metricSpecStrings.append(
          _generateMetricSpecString(inferenceElement=InferenceElement.classification,
                                    metric=movingAverageBaselineName,
                                    params={'window':metricWindow
                                                  ,"errorMetric":"avg_err",
                                                  "mode_window":200})
          )


    # Custom Error Metric
    if not options["customErrorMetric"] == None :
      #If errorWindow is not specified, make it equal to the default window
      if not "errorWindow" in options["customErrorMetric"]:
        options["customErrorMetric"]["errorWindow"] = metricWindow
      optimizeMetricSpec = _generateMetricSpecString(
                                inferenceElement=InferenceElement.classification,
                                metric="custom",
                                params=options["customErrorMetric"])
      optimizeMetricLabel = ".*custom_error_metric.*"

      metricSpecStrings.append(optimizeMetricSpec)


  # -----------------------------------------------------------------------
  # If plug in the predictionSteps variable for any dynamically generated
  #  prediction steps
  if options['dynamicPredictionSteps']:
    for i in range(len(metricSpecStrings)):
      metricSpecStrings[i] = metricSpecStrings[i].replace(
          "'$REPLACE_ME'", "predictionSteps")
    optimizeMetricLabel = optimizeMetricLabel.replace(
        "'$REPLACE_ME'", ".*")
  return metricSpecStrings, optimizeMetricLabel