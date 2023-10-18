def logDiffExp(A, B, out=None):
  """ returns log(exp(A) - exp(B)). A and B are numpy arrays. values in A should be
  greater than or equal to corresponding values in B"""

  if out is None:
    out = numpy.zeros(A.shape)

  indicator1 = A >= B
  assert indicator1.all(), "Values in the first array should be greater than the values in the second"
  out[indicator1] = A[indicator1] + numpy.log(1 - numpy.exp(B[indicator1]-A[indicator1]))

  return out