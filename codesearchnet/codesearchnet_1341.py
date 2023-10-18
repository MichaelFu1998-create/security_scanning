def pickByDistribution(distribution, r=None):
  """
  Pick a value according to the provided distribution.

  Example:

  ::

    pickByDistribution([.2, .1])

  Returns 0 two thirds of the time and 1 one third of the time.

  :param distribution: Probability distribution. Need not be normalized.
  :param r: Instance of random.Random. Uses the system instance if one is
         not provided.
  """

  if r is None:
    r = random

  x = r.uniform(0, sum(distribution))
  for i, d in enumerate(distribution):
    if x <= d:
      return i
    x -= d