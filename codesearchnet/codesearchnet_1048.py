def numpyStr(array, format='%f', includeIndices=False, includeZeros=True):
  """ Pretty print a numpy matrix using the given format string for each
  value. Return the string representation

  Parameters:
  ------------------------------------------------------------
  array:    The numpy array to print. This can be either a 1D vector or 2D matrix
  format:   The format string to use for each value
  includeIndices: If true, include [row,col] label for each value
  includeZeros:   Can only be set to False if includeIndices is on.
                  If True, include 0 values in the print-out
                  If False, exclude 0 values from the print-out.


  """

  shape = array.shape
  assert (len(shape) <= 2)
  items = ['[']
  if len(shape) == 1:
    if includeIndices:
      format = '%d:' + format
      if includeZeros:
        rowItems = [format % (c,x) for (c,x) in enumerate(array)]
      else:
        rowItems = [format % (c,x) for (c,x) in enumerate(array) if x != 0]
    else:
      rowItems = [format % (x) for x in array]
    items.extend(rowItems)

  else:
    (rows, cols) = shape
    if includeIndices:
      format = '%d,%d:' + format

    for r in xrange(rows):
      if includeIndices:
        rowItems = [format % (r,c,x) for c,x in enumerate(array[r])]
      else:
        rowItems = [format % (x) for x in array[r]]
      if r > 0:
        items.append('')

      items.append('[')
      items.extend(rowItems)
      if r < rows-1:
        items.append(']\n')
      else:
        items.append(']')


  items.append(']')
  return ' '.join(items)