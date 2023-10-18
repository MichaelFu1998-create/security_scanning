def __getOptimizedMetricLabel(self):
    """ Get the label for the metric being optimized. This function also caches
    the label in the instance variable self._optimizedMetricLabel

    Parameters:
    -----------------------------------------------------------------------
    metricLabels:   A sequence of all the labels being computed for this model

    Returns:        The label for the metric being optmized over
    """
    matchingKeys = matchPatterns([self._optimizeKeyPattern],
                                  self._getMetricLabels())

    if len(matchingKeys) == 0:
      raise Exception("None of the generated metrics match the specified "
                      "optimization pattern: %s. Available metrics are %s" % \
                       (self._optimizeKeyPattern, self._getMetricLabels()))
    elif len(matchingKeys) > 1:
      raise Exception("The specified optimization pattern '%s' matches more "
              "than one metric: %s" % (self._optimizeKeyPattern, matchingKeys))

    return matchingKeys[0]