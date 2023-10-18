def indexFromCoordinates(coordinates, dimensions):
  """
  Translate coordinates into an index, using the given coordinate system.

  Similar to ``numpy.ravel_multi_index``.

  :param coordinates: (list of ints) A list of coordinates of length 
         ``dimensions.size()``.

  :param dimensions: (list of ints) The coordinate system.

  :returns: (int) The index of the point. The coordinates are expressed as a 
            single index by using the dimensions as a mixed radix definition. 
            For example, in dimensions 42x10, the point [1, 4] is index 
            1*420 + 4*10 = 460.
  """
  index = 0
  for i, dimension in enumerate(dimensions):
    index *= dimension
    index += coordinates[i]

  return index