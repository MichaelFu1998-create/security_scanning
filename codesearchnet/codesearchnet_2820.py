def configure(level=logging.INFO, logfile=None):
  """ Configure logger which dumps log on terminal

  :param level: logging level: info, warning, verbose...
  :type level: logging level
  :param logfile: log file name, default to None
  :type logfile: string
  :return: None
  :rtype: None
  """

  # Remove all the existing StreamHandlers to avoid duplicate
  for handler in Log.handlers:
    if isinstance(handler, logging.StreamHandler):
      Log.handlers.remove(handler)

  Log.setLevel(level)

  # if logfile is specified, FileHandler is used
  if logfile is not None:
    log_format = "[%(asctime)s] [%(levelname)s]: %(message)s"
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)
    Log.addHandler(file_handler)
  # otherwise, use StreamHandler to output to stream (stdout, stderr...)
  else:
    log_format = "[%(asctime)s] %(log_color)s[%(levelname)s]%(reset)s: %(message)s"
    # pylint: disable=redefined-variable-type
    formatter = colorlog.ColoredFormatter(fmt=log_format, datefmt=date_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    Log.addHandler(stream_handler)