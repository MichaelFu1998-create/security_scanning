def getCentreAndSpreadOffsets(spaceShape,
                              spreadShape,
                              stepSize=1):
  """
  Generates centre offsets and spread offsets for block-mode based training
  regimes - star, cross, block.

    Parameters:
    -----------------------------------------------
    spaceShape:   The (height, width) of the 2-D space to explore. This
                  sets the number of center-points.
    spreadShape:  The shape (height, width) of the area around each center-point
                  to explore.
    stepSize:     The step size. How big each step is, in pixels. This controls
                  *both* the spacing of the center-points within the block and the
                  points we explore around each center-point
    retval:       (centreOffsets, spreadOffsets)
  """


  from nupic.math.cross import cross
  # =====================================================================
  # Init data structures
  # What is the range on the X and Y offsets of the center points?
  shape = spaceShape
  # If the shape is (1,1), special case of just 1 center point
  if shape[0] == 1 and shape[1] == 1:
    centerOffsets = [(0,0)]
  else:
    xMin = -1 * (shape[1] // 2)
    xMax = xMin + shape[1] - 1
    xPositions = range(stepSize * xMin, stepSize * xMax + 1, stepSize)

    yMin = -1 * (shape[0] // 2)
    yMax = yMin + shape[0] - 1
    yPositions = range(stepSize * yMin, stepSize * yMax + 1, stepSize)

    centerOffsets = list(cross(yPositions, xPositions))

  numCenterOffsets = len(centerOffsets)
  print "centerOffsets:", centerOffsets

  # What is the range on the X and Y offsets of the spread points?
  shape = spreadShape
  # If the shape is (1,1), special case of no spreading around each center
  #  point
  if shape[0] == 1 and shape[1] == 1:
    spreadOffsets = [(0,0)]
  else:
    xMin = -1 * (shape[1] // 2)
    xMax = xMin + shape[1] - 1
    xPositions = range(stepSize * xMin, stepSize * xMax + 1, stepSize)

    yMin = -1 * (shape[0] // 2)
    yMax = yMin + shape[0] - 1
    yPositions = range(stepSize * yMin, stepSize * yMax + 1, stepSize)

    spreadOffsets = list(cross(yPositions, xPositions))

    # Put the (0,0) entry first
    spreadOffsets.remove((0,0))
    spreadOffsets.insert(0, (0,0))

  numSpreadOffsets = len(spreadOffsets)
  print "spreadOffsets:", spreadOffsets

  return centerOffsets, spreadOffsets