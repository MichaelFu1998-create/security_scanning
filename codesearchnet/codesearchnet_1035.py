def _listOfOnTimesInVec(vector):
  """
  Returns 3 things for a vector:
    * the total on time
    * the number of runs
    * a list of the durations of each run.

  Parameters:
  -----------------------------------------------
  input stream: 11100000001100000000011111100000
  return value: (11, 3, [3, 2, 6])
  """

  # init counters
  durations = []
  numOnTimes   = 0
  totalOnTime = 0

  # Find where the nonzeros are
  nonzeros = numpy.array(vector).nonzero()[0]

  # Nothing to do if vector is empty
  if len(nonzeros) == 0:
    return (0, 0, [])

  # Special case of only 1 on bit
  if len(nonzeros) == 1:
    return (1, 1, [1])

  # Count the consecutive non-zeros
  prev = nonzeros[0]
  onTime = 1
  endIdx = nonzeros[-1]
  for idx in nonzeros[1:]:
    if idx != prev+1:
      totalOnTime += onTime
      numOnTimes  += 1
      durations.append(onTime)
      onTime       = 1
    else:
      onTime += 1
    prev = idx

  # Add in the last one
  totalOnTime += onTime
  numOnTimes  += 1
  durations.append(onTime)

  return (totalOnTime, numOnTimes, durations)