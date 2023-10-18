def computeSaturationLevels(outputs, outputsShape, sparseForm=False):
  """
  Compute the saturation for a continuous level. This breaks the level into
  multiple regions and computes the saturation level for each region.

  Parameters:
  --------------------------------------------
  outputs:      output of the level. If sparseForm is True, this is a list of
                  the non-zeros. If sparseForm is False, it is the dense
                  representation
  outputsShape: The shape of the outputs of the level (height, width)
  retval:       (sat, innerSat):
                  sat: list of the saturation levels of each non-empty
                    region of the level (each 0 -> 1.0)
                  innerSat: list of the saturation level of each non-empty region
                       that is not near an edge (each 0 -> 1.0)

  """

  # Get the outputs into a SparseBinaryMatrix
  if not sparseForm:
    outputs = outputs.reshape(outputsShape)
    spOut = SM32(outputs)
  else:
    if len(outputs) > 0:
      assert (outputs.max() < outputsShape[0] * outputsShape[1])
    spOut = SM32(1, outputsShape[0] * outputsShape[1])
    spOut.setRowFromSparse(0, outputs, [1]*len(outputs))
    spOut.reshape(outputsShape[0], outputsShape[1])

  # Get the activity in each local region using the nNonZerosPerBox method
  # This method takes a list of the end row indices and a list of the end
  #  column indices.
  # We will use regions that are 15x15, which give us about a 1/225 (.4%) resolution
  #  on saturation.
  regionSize = 15
  rows = xrange(regionSize+1, outputsShape[0]+1, regionSize)
  cols = xrange(regionSize+1, outputsShape[1]+1, regionSize)
  regionSums = spOut.nNonZerosPerBox(rows, cols)

  # Get all the nonzeros out - those are our saturation sums
  (locations, values) = regionSums.tolist()
  values /= float(regionSize * regionSize)
  sat = list(values)

  # Now, to compute which are the inner regions, we will only take the ones that
  #  are surrounded by activity above, below, left and right
  innerSat = []
  locationSet = set(locations)
  for (location, value) in itertools.izip(locations, values):
    (row, col) = location
    if (row-1,col) in locationSet and (row, col-1) in locationSet \
      and (row+1, col) in locationSet and (row, col+1) in locationSet:
      innerSat.append(value)


  return (sat, innerSat)