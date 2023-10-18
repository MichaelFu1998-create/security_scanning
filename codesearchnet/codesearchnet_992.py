def coordinatesFromIndex(index, dimensions):
  """
  Translate an index into coordinates, using the given coordinate system.

  Similar to ``numpy.unravel_index``.

  :param index: (int) The index of the point. The coordinates are expressed as a 
         single index by using the dimensions as a mixed radix definition. For 
         example, in dimensions 42x10, the point [1, 4] is index 
         1*420 + 4*10 = 460.

  :param dimensions (list of ints) The coordinate system.

  :returns: (list) of coordinates of length ``len(dimensions)``.
  """
  coordinates = [0] * len(dimensions)

  shifted = index
  for i in xrange(len(dimensions) - 1, 0, -1):
    coordinates[i] = shifted % dimensions[i]
    shifted = shifted / dimensions[i]

  coordinates[0] = shifted

  return coordinates