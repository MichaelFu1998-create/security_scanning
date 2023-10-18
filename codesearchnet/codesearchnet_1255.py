def getMetrics(self):
    """ 
    Gets the current metric values

    :returns: (dict) where each key is the metric-name, and the values are
              it scalar value. Same as the output of 
              :meth:`~nupic.frameworks.opf.prediction_metrics_manager.MetricsManager.update`
    """

    result = {}

    for metricObj, label in zip(self.__metrics, self.__metricLabels):
      value = metricObj.getMetric()
      result[label] = value['value']

    return result