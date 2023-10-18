def _rangeGen(data, std=1):
  """
  Return reasonable min/max values to use given the data.
  """
  dataStd = np.std(data)
  if dataStd == 0:
    dataStd = 1
  minval = np.min(data) -  std * dataStd
  maxval = np.max(data) +  std * dataStd
  return minval, maxval