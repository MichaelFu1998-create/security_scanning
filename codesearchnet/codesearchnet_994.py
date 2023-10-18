def neighborhood(centerIndex, radius, dimensions):
  """
  Get the points in the neighborhood of a point.

  A point's neighborhood is the n-dimensional hypercube with sides ranging
  [center - radius, center + radius], inclusive. For example, if there are two
  dimensions and the radius is 3, the neighborhood is 6x6. Neighborhoods are
  truncated when they are near an edge.

  This is designed to be fast. In C++ it's fastest to iterate through neighbors
  one by one, calculating them on-demand rather than creating a list of them.
  But in Python it's faster to build up the whole list in batch via a few calls
  to C code rather than calculating them on-demand with lots of calls to Python
  code.

  :param centerIndex: (int) The index of the point. The coordinates are 
         expressed as a single index by using the dimensions as a mixed radix 
         definition. For example, in dimensions 42x10, the point [1, 4] is index 
         1*420 + 4*10 = 460.

  :param radius: (int) The radius of this neighborhood about the 
         ``centerIndex``.

  :param dimensions: (indexable sequence) The dimensions of the world outside 
         this neighborhood.

  :returns: (numpy array) The points in the neighborhood, including 
            ``centerIndex``.
  """
  centerPosition = coordinatesFromIndex(centerIndex, dimensions)

  intervals = []
  for i, dimension in enumerate(dimensions):
    left = max(0, centerPosition[i] - radius)
    right = min(dimension - 1, centerPosition[i] + radius)
    intervals.append(xrange(left, right + 1))

  coords = numpy.array(list(itertools.product(*intervals)))
  return numpy.ravel_multi_index(coords.T, dimensions)