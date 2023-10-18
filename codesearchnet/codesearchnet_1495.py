def estimateNormal(sampleData, performLowerBoundCheck=True):
  """
  :param sampleData:
  :type sampleData: Numpy array.
  :param performLowerBoundCheck:
  :type performLowerBoundCheck: bool
  :returns: A dict containing the parameters of a normal distribution based on
      the ``sampleData``.
  """
  params = {
    "name": "normal",
    "mean": numpy.mean(sampleData),
    "variance": numpy.var(sampleData),
  }

  if performLowerBoundCheck:
    # Handle edge case of almost no deviations and super low anomaly scores. We
    # find that such low anomaly means can happen, but then the slightest blip
    # of anomaly score can cause the likelihood to jump up to red.
    if params["mean"] < 0.03:
      params["mean"] = 0.03

    # Catch all for super low variance to handle numerical precision issues
    if params["variance"] < 0.0003:
      params["variance"] = 0.0003

  # Compute standard deviation
  if params["variance"] > 0:
    params["stdev"] = math.sqrt(params["variance"])
  else:
    params["stdev"] = 0

  return params