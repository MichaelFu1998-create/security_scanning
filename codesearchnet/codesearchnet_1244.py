def generateRandomInput(numRecords, elemSize = 400, numSet = 42):
  """ Generates a set of input record

  Params:
          numRecords - how many records to generate
          elemSize - the size of each record (num 0s or 1s)
          numSet - how many 1s in each record

  Returns: a list of inputs
  """

  inputs = []

  for _ in xrange(numRecords):

    input = np.zeros(elemSize, dtype=realDType)
    for _ in range(0,numSet):
      ind = np.random.random_integers(0, elemSize-1, 1)[0]
      input[ind] = 1
    while abs(input.sum() - numSet) > 0.1:
      ind = np.random.random_integers(0, elemSize-1, 1)[0]
      input[ind] = 1

    inputs.append(input)

  return inputs