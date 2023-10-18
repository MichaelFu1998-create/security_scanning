def getRandomWithMods(inputSpace, maxChanges):
  """ Returns a random selection from the inputSpace with randomly modified
  up to maxChanges number of bits.
  """
  size = len(inputSpace)
  ind = np.random.random_integers(0, size-1, 1)[0]

  value = copy.deepcopy(inputSpace[ind])

  if maxChanges == 0:
    return value

  return modifyBits(value, maxChanges)