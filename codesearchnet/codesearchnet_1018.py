def addNoise(input, noise=0.1, doForeground=True, doBackground=True):
  """
  Add noise to the given input.

  Parameters:
  -----------------------------------------------
  input:         the input to add noise to
  noise:         how much noise to add
  doForeground:  If true, turn off some of the 1 bits in the input
  doBackground:  If true, turn on some of the 0 bits in the input

  """
  if doForeground and doBackground:
    return numpy.abs(input -  (numpy.random.random(input.shape) < noise))
  else:
    if doForeground:
      return numpy.logical_and(input, numpy.random.random(input.shape) > noise)
    if doBackground:
      return numpy.logical_or(input, numpy.random.random(input.shape) < noise)
  return input