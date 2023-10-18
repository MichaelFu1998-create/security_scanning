def generateSimpleCoincMatrix(nCoinc=10, length=500, activity=50):
  """
  Generate a non overlapping coincidence matrix. This is used to generate random
  inputs to the temporal learner and to compare the predicted output against.

  It generates a matrix of nCoinc rows, each row has length 'length' and has
  a total of 'activity' bits on.

  Parameters:
  -----------------------------------------------
  nCoinc:        the number of rows to generate
  length:        the length of each row
  activity:      the number of ones to put into each row.

  """
  assert nCoinc*activity<=length, "can't generate non-overlapping coincidences"
  coincMatrix = SM32(0, length)
  coinc = numpy.zeros(length, dtype='int32')

  for i in xrange(nCoinc):
      coinc[:] = 0
      coinc[i*activity:(i+1)*activity] = 1
      coincMatrix.addRow(coinc)

  return coincMatrix