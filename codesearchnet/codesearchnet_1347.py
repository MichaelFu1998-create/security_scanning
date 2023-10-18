def Distribution(pos, size, counts, dtype):
  """
  Returns an array of length size and type dtype that is everywhere 0,
  except in the indices listed in sequence pos.  The non-zero indices
  contain a normalized distribution based on the counts.


  :param pos:    A single integer or sequence of integers that specify
          the position of ones to be set.
  :param size:   The total size of the array to be returned.
  :param counts: The number of times we have observed each index.
  :param dtype:  The element type (compatible with NumPy array())
          of the array to be returned.
  :returns: An array of length size and element type dtype.
  """
  x = numpy.zeros(size, dtype=dtype)
  if hasattr(pos, '__iter__'):
    # calculate normalization constant
    total = 0
    for i in pos:
      total += counts[i]
    total = float(total)
    # set included positions to normalized probability
    for i in pos:
      x[i] = counts[i]/total
  # If we don't have a set of positions, assume there's only one position
  else: x[pos] = 1
  return x