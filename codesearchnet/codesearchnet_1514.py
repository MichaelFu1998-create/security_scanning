def lscsum(lx, epsilon=None):
  """
  Accepts log-values as input, exponentiates them, computes the sum,
  then converts the sum back to log-space and returns the result.
  Handles underflow by rescaling so that the largest values is exactly 1.0.
  """
  lx = numpy.asarray(lx)
  base = lx.max()

  # If the input is the log of 0's, catch this condition before we generate
  #  an exception, and return the log(0)
  if numpy.isinf(base):
    return base

  # If the user specified an epsilon and we are below it, return epsilon
  if (epsilon is not None) and (base < epsilon):
    return epsilon

  x = numpy.exp(lx - base)
  ssum = x.sum()

  result = numpy.log(ssum) + base
  # try:
  #   conventional = numpy.log(numpy.exp(lx).sum())
  #   if not similar(result, conventional):
  #     if numpy.isinf(conventional).any() and not numpy.isinf(result).any():
  #       # print "Scaled log sum avoided underflow or overflow."
  #       pass
  #     else:
  #       import sys
  #       print >>sys.stderr, "Warning: scaled log sum did not match."
  #       print >>sys.stderr, "Scaled log result:"
  #       print >>sys.stderr, result
  #       print >>sys.stderr, "Conventional result:"
  #       print >>sys.stderr, conventional
  # except FloatingPointError, e:
  #   # print "Scaled log sum avoided underflow or overflow."
  #   pass

  return result