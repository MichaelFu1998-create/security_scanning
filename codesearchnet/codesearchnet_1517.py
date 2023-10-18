def nsum0(lx):
  """
  Accepts log-values as input, exponentiates them, sums down the rows
  (first dimension), normalizes and returns the result.
  Handles underflow by rescaling so that the largest values is exactly 1.0.
  """
  lx = numpy.asarray(lx)
  base = lx.max()
  x = numpy.exp(lx - base)
  ssum = x.sum(0)
  result = ssum / ssum.sum()

  conventional = (numpy.exp(lx).sum(0) / numpy.exp(lx).sum())
  assert similar(result, conventional)

  return result