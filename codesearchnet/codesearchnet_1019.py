def generateCoincMatrix(nCoinc=10, length=500, activity=50):
  """
  Generate a coincidence matrix. This is used to generate random inputs to the
  temporal learner and to compare the predicted output against.

  It generates a matrix of nCoinc rows, each row has length 'length' and has
  a total of 'activity' bits on.

  Parameters:
  -----------------------------------------------
  nCoinc:        the number of rows to generate
  length:        the length of each row
  activity:      the number of ones to put into each row.

  """

  coincMatrix0 = SM32(int(nCoinc), int(length))
  theOnes = numpy.array([1.0] * activity, dtype=numpy.float32)
  for rowIdx in xrange(nCoinc):
    coinc = numpy.array(random.sample(xrange(length),
                activity), dtype=numpy.uint32)
    coinc.sort()
    coincMatrix0.setRowFromSparse(rowIdx, coinc, theOnes)

  # This is the right code to use, it's faster, but it derails the unit
  # testing of the pooling for now.
  coincMatrix = SM32(int(nCoinc), int(length))
  coincMatrix.initializeWithFixedNNZR(activity)

  return coincMatrix0