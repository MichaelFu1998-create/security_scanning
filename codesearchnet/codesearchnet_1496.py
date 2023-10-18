def tailProbability(x, distributionParams):
  """
  Given the normal distribution specified by the mean and standard deviation
  in distributionParams, return the probability of getting samples further
  from the mean. For values above the mean, this is the probability of getting
  samples > x and for values below the mean, the probability of getting
  samples < x. This is the Q-function: the tail probability of the normal distribution.

  :param distributionParams: dict with 'mean' and 'stdev' of the distribution
  """
  if "mean" not in distributionParams or "stdev" not in distributionParams:
    raise RuntimeError("Insufficient parameters to specify the distribution.")

  if x < distributionParams["mean"]:
    # Gaussian is symmetrical around mean, so flip to get the tail probability
    xp = 2 * distributionParams["mean"] - x
    return tailProbability(xp, distributionParams)

  # Calculate the Q function with the complementary error function, explained
  # here: http://www.gaussianwaves.com/2012/07/q-function-and-error-functions
  z = (x - distributionParams["mean"]) / distributionParams["stdev"]
  return 0.5 * math.erfc(z/1.4142)