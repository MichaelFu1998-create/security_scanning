def normalize(lx):
  """
  Accepts log-values as input, exponentiates them,
  normalizes and returns the result.
  Handles underflow by rescaling so that the largest values is exactly 1.0.
  """
  lx = numpy.asarray(lx)
  base = lx.max()
  x = numpy.exp(lx - base)
  result = x / x.sum()

  conventional = (numpy.exp(lx) / numpy.exp(lx).sum())
  assert similar(result, conventional)

  return result