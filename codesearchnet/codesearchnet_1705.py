def logExceptions(logger=None):
  """ Returns a closure suitable for use as function/method decorator for
  logging exceptions that leave the scope of the decorated function. Exceptions
  are logged at ERROR level.

  logger:    user-supplied logger instance. Defaults to logging.getLogger.

  Usage Example:
    NOTE: logging must be initialized *before* any loggers are created, else
      there will be no output; see nupic.support.initLogging()

    @logExceptions()
    def myFunctionFoo():
        ...
        raise RuntimeError("something bad happened")
        ...
  """
  logger = (logger if logger is not None else logging.getLogger(__name__))

  def exceptionLoggingDecorator(func):
    @functools.wraps(func)
    def exceptionLoggingWrap(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      except:
        logger.exception(
          "Unhandled exception %r from %r. Caller stack:\n%s",
          sys.exc_info()[1], func, ''.join(traceback.format_stack()), )
        raise

    return exceptionLoggingWrap

  return exceptionLoggingDecorator