def anomalyProbability(self, value, anomalyScore, timestamp=None):
    """
    Compute the probability that the current value plus anomaly score represents
    an anomaly given the historical distribution of anomaly scores. The closer
    the number is to 1, the higher the chance it is an anomaly.

    :param value: the current metric ("raw") input value, eg. "orange", or
                   '21.2' (deg. Celsius), ...
    :param anomalyScore: the current anomaly score
    :param timestamp: [optional] timestamp of the ocurrence,
                       default (None) results in using iteration step.
    :returns: the anomalyLikelihood for this record.
    """
    if timestamp is None:
      timestamp = self._iteration

    dataPoint = (timestamp, value, anomalyScore)
    # We ignore the first probationaryPeriod data points
    if self._iteration < self._probationaryPeriod:
      likelihood = 0.5
    else:
      # On a rolling basis we re-estimate the distribution
      if ( (self._distribution is None) or
           (self._iteration % self._reestimationPeriod == 0) ):

        numSkipRecords = self._calcSkipRecords(
          numIngested=self._iteration,
          windowSize=self._historicalScores.maxlen,
          learningPeriod=self._learningPeriod)

        _, _, self._distribution = estimateAnomalyLikelihoods(
          self._historicalScores,
          skipRecords=numSkipRecords)

      likelihoods, _, self._distribution = updateAnomalyLikelihoods(
        [dataPoint],
        self._distribution)

      likelihood = 1.0 - likelihoods[0]

    # Before we exit update historical scores and iteration
    self._historicalScores.append(dataPoint)
    self._iteration += 1

    return likelihood