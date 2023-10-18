def MultiIndicator(pos, size, dtype):
  """
  Returns an array of length size and type dtype that is everywhere 0,
  except in the indices listed in sequence pos.

  :param pos:   A single integer or sequence of integers that specify
         the position of ones to be set.
  :param size:  The total size of the array to be returned.
  :param dtype: The element type (compatible with NumPy array())
         of the array to be returned.
  :returns: An array of length size and element type dtype.
  """
  x = numpy.zeros(size, dtype=dtype)
  if hasattr(pos, '__iter__'):
    for i in pos: x[i] = 1
  else: x[pos] = 1
  return x