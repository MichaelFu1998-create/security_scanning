def resetVector(x1, x2):
  """
  Copies the contents of vector x1 into vector x2.

  @param x1 (array) binary vector to be copied
  @param x2 (array) binary vector where x1 is copied
  """
  size = len(x1)
  for i in range(size):
    x2[i] = x1[i]