def getMetricDetails(self, metricLabel):
    """ 
    Gets detailed info about a given metric, in addition to its value. This
    may including any statistics or auxilary data that are computed for a given
    metric.

    :param metricLabel: (string) label of the given metric (see 
           :class:`~nupic.frameworks.opf.metrics.MetricSpec`)

    :returns: (dict) of metric information, as returned by 
             :meth:`nupic.frameworks.opf.metrics.MetricsIface.getMetric`.
    """
    try:
      metricIndex = self.__metricLabels.index(metricLabel)
    except IndexError:
      return None

    return self.__metrics[metricIndex].getMetric()