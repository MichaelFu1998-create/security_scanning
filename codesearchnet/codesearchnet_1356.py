def getModule(metricSpec):
  """
  Factory method to return an appropriate :class:`MetricsIface` module.
  
  - ``rmse``: :class:`MetricRMSE`
  - ``nrmse``: :class:`MetricNRMSE`
  - ``aae``: :class:`MetricAAE`
  - ``acc``: :class:`MetricAccuracy`
  - ``avg_err``: :class:`MetricAveError`
  - ``trivial``: :class:`MetricTrivial`
  - ``two_gram``: :class:`MetricTwoGram`
  - ``moving_mean``: :class:`MetricMovingMean`
  - ``moving_mode``: :class:`MetricMovingMode`
  - ``neg_auc``: :class:`MetricNegAUC`
  - ``custom_error_metric``: :class:`CustomErrorMetric`
  - ``multiStep``: :class:`MetricMultiStep`
  - ``ms_aae``: :class:`MetricMultiStepAAE`
  - ``ms_avg_err``: :class:`MetricMultiStepAveError`
  - ``passThruPrediction``: :class:`MetricPassThruPrediction`
  - ``altMAPE``: :class:`MetricAltMAPE`
  - ``MAPE``: :class:`MetricMAPE`
  - ``multi``: :class:`MetricMulti`
  - ``negativeLogLikelihood``: :class:`MetricNegativeLogLikelihood`
  
  :param metricSpec: (:class:`MetricSpec`) metric to find module for. 
         ``metricSpec.metric`` must be in the list above.
  
  :returns: (:class:`AggregateMetric`) an appropriate metric module
  """

  metricName = metricSpec.metric

  if metricName == 'rmse':
    return MetricRMSE(metricSpec)
  if metricName == 'nrmse':
    return MetricNRMSE(metricSpec)
  elif metricName == 'aae':
    return MetricAAE(metricSpec)
  elif metricName == 'acc':
    return MetricAccuracy(metricSpec)
  elif metricName == 'avg_err':
    return MetricAveError(metricSpec)
  elif metricName == 'trivial':
    return MetricTrivial(metricSpec)
  elif metricName == 'two_gram':
    return MetricTwoGram(metricSpec)
  elif metricName == 'moving_mean':
    return MetricMovingMean(metricSpec)
  elif metricName == 'moving_mode':
    return MetricMovingMode(metricSpec)
  elif metricName == 'neg_auc':
    return MetricNegAUC(metricSpec)
  elif metricName == 'custom_error_metric':
    return CustomErrorMetric(metricSpec)
  elif metricName == 'multiStep':
    return MetricMultiStep(metricSpec)
  elif metricName == 'multiStepProbability':
    return MetricMultiStepProbability(metricSpec)
  elif metricName == 'ms_aae':
    return MetricMultiStepAAE(metricSpec)
  elif metricName == 'ms_avg_err':
    return MetricMultiStepAveError(metricSpec)
  elif metricName == 'passThruPrediction':
    return MetricPassThruPrediction(metricSpec)
  elif metricName == 'altMAPE':
    return MetricAltMAPE(metricSpec)
  elif metricName == 'MAPE':
    return MetricMAPE(metricSpec)
  elif metricName == 'multi':
    return MetricMulti(metricSpec)
  elif metricName == 'negativeLogLikelihood':
    return MetricNegativeLogLikelihood(metricSpec)
  else:
    raise Exception("Unsupported metric type: %s" % metricName)