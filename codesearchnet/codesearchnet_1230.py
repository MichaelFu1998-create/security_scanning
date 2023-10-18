def setLoggedMetrics(self, metricNames):
    """ Tell the writer which metrics should be written

    Parameters:
    -----------------------------------------------------------------------
    metricsNames: A list of metric lables to be written
    """
    if metricNames is None:
      self.__metricNames = set([])
    else:
      self.__metricNames = set(metricNames)