def initLogger(obj):
  """
  Helper function to create a logger object for the current object with
  the standard Numenta prefix.

  :param obj: (object) to add a logger to
  """
  if inspect.isclass(obj):
    myClass = obj
  else:
    myClass = obj.__class__
  logger = logging.getLogger(".".join(
    ['com.numenta', myClass.__module__, myClass.__name__]))
  return logger