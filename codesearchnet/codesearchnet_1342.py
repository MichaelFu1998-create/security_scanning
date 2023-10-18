def Indicator(pos, size, dtype):
  """
  Returns an array of length size and type dtype that is everywhere 0,
  except in the index in pos.

  :param pos: (int) specifies the position of the one entry that will be set.
  :param size: (int) The total size of the array to be returned.
  :param dtype: The element type (compatible with NumPy array())
         of the array to be returned.
  :returns: (list) of length ``size`` and element type ``dtype``.
  """
  x = numpy.zeros(size, dtype=dtype)
  x[pos] = 1
  return x