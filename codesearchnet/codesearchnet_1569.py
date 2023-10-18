def corruptVector(v1, noiseLevel, numActiveCols):
  """
  Corrupts a copy of a binary vector by inverting noiseLevel percent of its bits.
  
  @param v1      (array) binary vector whose copy will be corrupted
  @param noiseLevel  (float) amount of noise to be applied on the new vector
  @param numActiveCols (int)   number of sparse columns that represent an input
  
  @return v2 (array) corrupted binary vector
  """  
  size = len(v1)
  v2 = np.zeros(size, dtype="uint32")
  bitsToSwap = int(noiseLevel * numActiveCols)
  # Copy the contents of v1 into v2
  for i in range(size):
    v2[i] = v1[i]
  for _ in range(bitsToSwap):
    i = random.randrange(size)
    if v2[i] == 1:
      v2[i] = 0
    else:
      v2[i] = 1
  return v2