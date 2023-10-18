def generatePlot(outputs, origData):
  """ Generates a table where each cell represent a frequency of pairs
  as described below.
  x coordinate is the % difference between input records (origData list),
  y coordinate is the % difference between corresponding output records.
  """

  PLOT_PRECISION = 100

  distribMatrix = np.zeros((PLOT_PRECISION+1,PLOT_PRECISION+1))

  outputSize = len(outputs)

  for i in range(0,outputSize):
    for j in range(i+1,outputSize):

      in1 = outputs[i]
      in2 = outputs[j]
      dist = (abs(in1-in2) > 0.1)
      intDist = int(dist.sum()/2+0.1)

      orig1 = origData[i]
      orig2 = origData[j]
      origDist = (abs(orig1-orig2) > 0.1)
      intOrigDist = int(origDist.sum()/2+0.1)

      if intDist < 2 and intOrigDist > 10:
        print 'Elements %d,%d has very small SP distance: %d' % (i, j, intDist)
        print 'Input elements distance is %d' % intOrigDist

      x = int(PLOT_PRECISION*intDist/40.0)
      y = int(PLOT_PRECISION*intOrigDist/42.0)
      if distribMatrix[x, y] < 0.1:
        distribMatrix[x, y] = 3
      else:
        if distribMatrix[x, y] < 10:
          distribMatrix[x, y] += 1

  # Add some elements for the scale drawing
  distribMatrix[4, 50] = 3
  distribMatrix[4, 52] = 4
  distribMatrix[4, 54] = 5
  distribMatrix[4, 56] = 6
  distribMatrix[4, 58] = 7
  distribMatrix[4, 60] = 8
  distribMatrix[4, 62] = 9
  distribMatrix[4, 64] = 10

  return distribMatrix