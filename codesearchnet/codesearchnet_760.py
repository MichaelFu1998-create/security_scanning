def _getLogger(cls, logLevel=None):
  """ Gets a logger for the given class in this module
  """
  logger = logging.getLogger(
    ".".join(['com.numenta', _MODULE_NAME, cls.__name__]))

  if logLevel is not None:
    logger.setLevel(logLevel)

  return logger