def profileSP(spClass, spDim, nRuns):
  """
  profiling performance of SpatialPooler (SP)
  using the python cProfile module and ordered by cumulative time,
  see how to run on command-line above.

  @param spClass implementation of SP (cpp, py, ..)
  @param spDim number of columns in SP (in 1D, for 2D see colDim in code)
  @param nRuns number of calls of the profiled code (epochs)
  """
  # you can change dimensionality here, eg to 2D
  inDim = [10000, 1, 1]
  colDim = [spDim, 1, 1]


  # create SP instance to measure
  # changing the params here affects the performance
  sp = spClass(
        inputDimensions=inDim,
        columnDimensions=colDim,
        potentialRadius=3,
        potentialPct=0.5,
        globalInhibition=False,
        localAreaDensity=-1.0,
        numActiveColumnsPerInhArea=3,
        stimulusThreshold=1,
        synPermInactiveDec=0.01,
        synPermActiveInc=0.1,
        synPermConnected=0.10,
        minPctOverlapDutyCycle=0.1,
        dutyCyclePeriod=10,
        boostStrength=10.0,
        seed=42,
        spVerbosity=0)


  # generate input data
  dataDim = inDim
  dataDim.append(nRuns)
  data = numpy.random.randint(0, 2, dataDim).astype('float32')

  for i in xrange(nRuns):
    # new data every time, this is the worst case performance
    # real performance would be better, as the input data would not be completely random
    d = data[:,:,:,i]
    activeArray = numpy.zeros(colDim)

    # the actual function to profile!
    sp.compute(d, True, activeArray)