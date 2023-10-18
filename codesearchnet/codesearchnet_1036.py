def _fillInOnTimes(vector, durations):
  """
  Helper function used by averageOnTimePerTimestep. 'durations' is a vector
  which must be the same len as vector. For each "on" in vector, it fills in
  the corresponding element of duration with the duration of that "on" signal
  up until that time

  Parameters:
  -----------------------------------------------
  vector:     vector of output values over time
  durations:  vector same length as 'vector', initialized to 0's.
              This is filled in with the durations of each 'on" signal.

  Example:
  vector:     11100000001100000000011111100000
  durations:  12300000001200000000012345600000
  """

  # Find where the nonzeros are
  nonzeros = numpy.array(vector).nonzero()[0]

  # Nothing to do if vector is empty
  if len(nonzeros) == 0:
    return

  # Special case of only 1 on bit
  if len(nonzeros) == 1:
    durations[nonzeros[0]] = 1
    return

  # Count the consecutive non-zeros
  prev = nonzeros[0]
  onTime = 1
  onStartIdx = prev
  endIdx = nonzeros[-1]
  for idx in nonzeros[1:]:
    if idx != prev+1:
      # Fill in the durations
      durations[onStartIdx:onStartIdx+onTime] = range(1,onTime+1)
      onTime       = 1
      onStartIdx = idx
    else:
      onTime += 1
    prev = idx

  # Fill in the last one
  durations[onStartIdx:onStartIdx+onTime] = range(1,onTime+1)