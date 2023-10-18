def generateVectors(numVectors=100, length=500, activity=50):
  """
  Generate a list of random sparse distributed vectors.  This is used to generate
  training vectors to the spatial or temporal learner and to compare the predicted
  output against.

  It generates a list of 'numVectors' elements, each element has length 'length'
  and has a total of 'activity' bits on.

  Parameters:
  -----------------------------------------------
  numVectors:    the number of vectors to generate
  length:        the length of each row
  activity:      the number of ones to put into each row.

  """

  vectors = []
  coinc = numpy.zeros(length, dtype='int32')
  indexList = range(length)

  for i in xrange(numVectors):
      coinc[:] = 0
      coinc[random.sample(indexList, activity)] = 1
      vectors.append(coinc.copy())

  return vectors