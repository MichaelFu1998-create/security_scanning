def tmDiff(tm1, tm2, verbosity = 0, relaxSegmentTests =True):
  """
  Given two TM instances, list the difference between them and returns False
  if there is a difference. This function checks the major parameters. If this
  passes (and checkLearn is true) it checks the number of segments on
  each cell. If this passes, checks each synapse on each segment.
  When comparing C++ and Py, the segments are usually in different orders in the
  cells. tmDiff ignores segment order when comparing TM's.

  """

  # First check basic parameters. If we fail here, don't continue
  if sameTMParams(tm1, tm2) == False:
    print "Two TM's have different parameters"
    return False

  result = True

  # Compare states at t first, they usually diverge before the structure of the
  # cells starts diverging

  if (tm1.activeState['t'] != tm2.activeState['t']).any():
    print 'Active states diverge', numpy.where(tm1.activeState['t'] != tm2.activeState['t'])
    result = False

  if (tm1.predictedState['t'] - tm2.predictedState['t']).any():
    print 'Predicted states diverge', numpy.where(tm1.predictedState['t'] != tm2.predictedState['t'])
    result = False

  # TODO: check confidence at T (confT)

  # Now check some high level learned parameters.
  if tm1.getNumSegments() != tm2.getNumSegments():
    print "Number of segments are different", tm1.getNumSegments(), tm2.getNumSegments()
    result = False

  if tm1.getNumSynapses() != tm2.getNumSynapses():
    print "Number of synapses are different", tm1.getNumSynapses(), tm2.getNumSynapses()
    tm1.printCells()
    tm2.printCells()
    result = False

  # Check that each cell has the same number of segments and synapses
  for c in xrange(tm1.numberOfCols):
    for i in xrange(tm2.cellsPerColumn):
      if tm1.getNumSegmentsInCell(c, i) != tm2.getNumSegmentsInCell(c, i):
        print "Num segments different in cell:",c,i,
        print tm1.getNumSegmentsInCell(c, i), tm2.getNumSegmentsInCell(c, i)
        result = False

  # If the above tests pass, then check each segment and report differences
  # Note that segments in tm1 can be in a different order than tm2. Here we
  # make sure that, for each segment in tm1, there is an identical segment
  # in tm2.
  if result == True and not relaxSegmentTests:
    for c in xrange(tm1.numberOfCols):
      for i in xrange(tm2.cellsPerColumn):
        nSegs = tm1.getNumSegmentsInCell(c, i)
        for segIdx in xrange(nSegs):
          tm1seg = tm1.getSegmentOnCell(c, i, segIdx)

          # Loop through all segments in tm2seg and see if any of them match tm1seg
          res = False
          for tm2segIdx in xrange(nSegs):
            tm2seg = tm2.getSegmentOnCell(c, i, tm2segIdx)
            if sameSegment(tm1seg, tm2seg) == True:
              res = True
              break
          if res == False:
            print "\nSegments are different for cell:",c,i
            if verbosity >= 1:
              print "C++"
              tm1.printCell(c, i)
              print "Py"
              tm2.printCell(c, i)
            result = False

  if result == True and (verbosity > 1):
    print "TM's match"

  return result