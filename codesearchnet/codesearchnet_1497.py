def isValidEstimatorParams(p):
  """
  :returns: ``True`` if ``p`` is a valid estimator params as might be returned
    by ``estimateAnomalyLikelihoods()`` or ``updateAnomalyLikelihoods``,
    ``False`` otherwise.  Just does some basic validation.
  """
  if not isinstance(p, dict):
    return False
  if "distribution" not in p:
    return False
  if "movingAverage" not in p:
    return False
  dist = p["distribution"]
  if not ("mean" in dist and "name" in dist
          and "variance" in dist and "stdev" in dist):
    return False

  return True