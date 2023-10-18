def clippedObj(obj, maxElementSize=64):
  """
  Return a clipped version of obj suitable for printing, This
  is useful when generating log messages by printing data structures, but
  don't want the message to be too long.

  If passed in a dict, list, or namedtuple, each element of the structure's
  string representation will be limited to 'maxElementSize' characters. This
  will return a new object where the string representation of each element
  has been truncated to fit within maxElementSize.
  """

  # Is it a named tuple?
  if hasattr(obj, '_asdict'):
    obj = obj._asdict()


  # Printing a dict?
  if isinstance(obj, dict):
    objOut = dict()
    for key,val in obj.iteritems():
      objOut[key] = clippedObj(val)

  # Printing a list?
  elif hasattr(obj, '__iter__'):
    objOut = []
    for val in obj:
      objOut.append(clippedObj(val))

  # Some other object
  else:
    objOut = str(obj)
    if len(objOut) > maxElementSize:
      objOut = objOut[0:maxElementSize] + '...'

  return objOut