def log_error(msg=None, exc_info=None, logger=None, **kwargs):
    """
        log an exception and its traceback on the logger defined

    Parameters
    ----------
    msg : str, optional
        A message to add to the error
    exc_info : tuple
        Information about the current exception
    logger : logging.Logger
        logger to use
    """
    if logger is None:
        logger = _logger

    if not exc_info:
        exc_info = sys.exc_info()

    if msg is None:
        msg = ""

    exc_class, exc_msg, _ = exc_info

    if all(info is not None for info in exc_info):
        logger.error(msg, exc_info=exc_info)