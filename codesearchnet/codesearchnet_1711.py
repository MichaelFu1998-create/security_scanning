def createTMs(includeCPP = True,
              includePy = True,
              numCols = 100,
              cellsPerCol = 4,
              activationThreshold = 3,
              minThreshold = 3,
              newSynapseCount = 3,
              initialPerm = 0.6,
              permanenceInc = 0.1,
              permanenceDec = 0.0,
              globalDecay = 0.0,
              pamLength = 0,
              checkSynapseConsistency = True,
              maxInfBacktrack = 0,
              maxLrnBacktrack = 0,
              **kwargs
              ):

  """Create one or more TM instances, placing each into a dict keyed by
  name.

  Parameters:
  ------------------------------------------------------------------
  retval:   tms - dict of TM instances
  """

  # Keep these fixed:
  connectedPerm = 0.5

  tms = dict()

  if includeCPP:
    if VERBOSITY >= 2:
      print "Creating BacktrackingTMCPP instance"

    cpp_tm = BacktrackingTMCPP(numberOfCols = numCols, cellsPerColumn = cellsPerCol,
                               initialPerm = initialPerm, connectedPerm = connectedPerm,
                               minThreshold = minThreshold, newSynapseCount = newSynapseCount,
                               permanenceInc = permanenceInc, permanenceDec = permanenceDec,
                               activationThreshold = activationThreshold,
                               globalDecay = globalDecay, burnIn = 1,
                               seed=SEED, verbosity=VERBOSITY,
                               checkSynapseConsistency = checkSynapseConsistency,
                               collectStats = True,
                               pamLength = pamLength,
                               maxInfBacktrack = maxInfBacktrack,
                               maxLrnBacktrack = maxLrnBacktrack,
                               )

    # Ensure we are copying over learning states for TMDiff
    cpp_tm.retrieveLearningStates = True

    tms['CPP'] = cpp_tm


  if includePy:
    if VERBOSITY >= 2:
      print "Creating PY TM instance"

    py_tm = BacktrackingTM(numberOfCols = numCols,
                           cellsPerColumn = cellsPerCol,
                           initialPerm = initialPerm,
                           connectedPerm = connectedPerm,
                           minThreshold = minThreshold,
                           newSynapseCount = newSynapseCount,
                           permanenceInc = permanenceInc,
                           permanenceDec = permanenceDec,
                           activationThreshold = activationThreshold,
                           globalDecay = globalDecay, burnIn = 1,
                           seed=SEED, verbosity=VERBOSITY,
                           collectStats = True,
                           pamLength = pamLength,
                           maxInfBacktrack = maxInfBacktrack,
                           maxLrnBacktrack = maxLrnBacktrack,
                           )


    tms['PY '] = py_tm

  return tms