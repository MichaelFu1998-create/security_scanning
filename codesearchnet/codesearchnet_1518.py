def logSumExp(A, B, out=None):
  """ returns log(exp(A) + exp(B)). A and B are numpy arrays"""

  if out is None:
    out = numpy.zeros(A.shape)

  indicator1 = A >= B
  indicator2 = numpy.logical_not(indicator1)
  out[indicator1] = A[indicator1] + numpy.log1p(numpy.exp(B[indicator1]-A[indicator1]))
  out[indicator2]  = B[indicator2] + numpy.log1p(numpy.exp(A[indicator2]-B[indicator2]))

  return out