def configure(level, logfile=None):
  """ configure logging """
  log_format = "%(asctime)s-%(levelname)s: %(message)s"
  date_format = '%a, %d %b %Y %H:%M:%S'

  logging.basicConfig(format=log_format, datefmt=date_format)
  Log.setLevel(level)

  if logfile is not None:
    fh = logging.FileHandler(logfile)
    fh.setFormatter(logging.Formatter(log_format))
    Log.addHandler(fh)