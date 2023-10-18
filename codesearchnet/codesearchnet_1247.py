def modifyBits(inputVal, maxChanges):
  """ Modifies up to maxChanges number of bits in the inputVal
  """
  changes = np.random.random_integers(0, maxChanges, 1)[0]

  if changes == 0:
    return inputVal

  inputWidth = len(inputVal)

  whatToChange = np.random.random_integers(0, 41, changes)

  runningIndex = -1
  numModsDone = 0
  for i in xrange(inputWidth):
    if numModsDone >= changes:
      break
    if inputVal[i] == 1:
      runningIndex += 1
      if runningIndex in whatToChange:
        if i != 0 and inputVal[i-1] == 0:
          inputVal[i-1] = 1
          inputVal[i] = 0

  return inputVal