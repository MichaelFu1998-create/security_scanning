def _calcSkipRecords(numIngested, windowSize, learningPeriod):
    """Return the value of skipRecords for passing to estimateAnomalyLikelihoods

    If `windowSize` is very large (bigger than the amount of data) then this
    could just return `learningPeriod`. But when some values have fallen out of
    the historical sliding window of anomaly records, then we have to take those
    into account as well so we return the `learningPeriod` minus the number
    shifted out.

    :param numIngested - (int) number of data points that have been added to the
      sliding window of historical data points.
    :param windowSize - (int) size of sliding window of historical data points.
    :param learningPeriod - (int) the number of iterations required for the
      algorithm to learn the basic patterns in the dataset and for the anomaly
      score to 'settle down'.
    """
    numShiftedOut = max(0, numIngested - windowSize)
    return min(numIngested, max(0, learningPeriod - numShiftedOut))