def compute(self, activeColumns, predictedColumns,
              inputValue=None, timestamp=None):
    """Compute the anomaly score as the percent of active columns not predicted.

    :param activeColumns: array of active column indices
    :param predictedColumns: array of columns indices predicted in this step
                             (used for anomaly in step T+1)
    :param inputValue: (optional) value of current input to encoders
                                  (eg "cat" for category encoder)
                                  (used in anomaly-likelihood)
    :param timestamp: (optional) date timestamp when the sample occured
                                 (used in anomaly-likelihood)
    :returns: the computed anomaly score; float 0..1
    """
    # Start by computing the raw anomaly score.
    anomalyScore = computeRawAnomalyScore(activeColumns, predictedColumns)

    # Compute final anomaly based on selected mode.
    if self._mode == Anomaly.MODE_PURE:
      score = anomalyScore
    elif self._mode == Anomaly.MODE_LIKELIHOOD:
      if inputValue is None:
        raise ValueError("Selected anomaly mode 'Anomaly.MODE_LIKELIHOOD' "
                 "requires 'inputValue' as parameter to compute() method. ")

      probability = self._likelihood.anomalyProbability(
          inputValue, anomalyScore, timestamp)
      # low likelihood -> hi anomaly
      score = 1 - probability
    elif self._mode == Anomaly.MODE_WEIGHTED:
      probability = self._likelihood.anomalyProbability(
          inputValue, anomalyScore, timestamp)
      score = anomalyScore * (1 - probability)

    # Last, do moving-average if windowSize was specified.
    if self._movingAverage is not None:
      score = self._movingAverage.next(score)

    # apply binary discretization if required
    if self._binaryThreshold is not None:
      if score >= self._binaryThreshold:
        score = 1.0
      else:
        score = 0.0

    return score