def init_logging(logger, log_file, log_level):
  """
  Initialize the naarad logger.
  :param: logger: logger object to initialize
  :param: log_file: log file name
  :param: log_level: log level (debug, info, warn, error)
  """
  with open(log_file, 'w'):
    pass
  numeric_level = getattr(logging, log_level.upper(), None) if log_level else logging.INFO
  if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % log_level)
  logger.setLevel(logging.DEBUG)
  fh = logging.FileHandler(log_file)
  fh.setLevel(logging.DEBUG)
  ch = logging.StreamHandler()
  ch.setLevel(numeric_level)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  fh.setFormatter(formatter)
  ch.setFormatter(formatter)
  logger.addHandler(fh)
  logger.addHandler(ch)
  return CONSTANTS.OK