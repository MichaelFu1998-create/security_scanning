def lscsum0(lx):
  """
  Accepts log-values as input, exponentiates them, sums down the rows
  (first dimension), then converts the sum back to log-space and returns the result.
  Handles underflow by rescaling so that the largest values is exactly 1.0.
  """
  # rows = lx.shape[0]
  # columns = numpy.prod(lx.shape[1:])
  # lx = lx.reshape(rows, columns)
  # bases = lx.max(1).reshape(rows, 1)
  # bases = lx.max(0).reshape((1,) + lx.shape[1:])
  lx = numpy.asarray(lx)
  bases = lx.max(0) # Don't need to reshape in the case of 0.
  x = numpy.exp(lx - bases)
  ssum = x.sum(0)

  result = numpy.log(ssum) + bases
  try:
    conventional = numpy.log(numpy.exp(lx).sum(0))

    if not similar(result, conventional):
      if numpy.isinf(conventional).any() and not numpy.isinf(result).any():
        # print "Scaled log sum down axis 0 avoided underflow or overflow."
        pass
      else:
        import sys
        print >>sys.stderr, "Warning: scaled log sum down axis 0 did not match."
        print >>sys.stderr, "Scaled log result:"
        print >>sys.stderr, result
        print >>sys.stderr, "Conventional result:"
        print >>sys.stderr, conventional
  except FloatingPointError, e:
    # print "Scaled log sum down axis 0 avoided underflow or overflow."
    pass


  return result