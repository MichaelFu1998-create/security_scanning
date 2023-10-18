def logEntryExit(getLoggerCallback=logging.getLogger,
                 entryExitLogLevel=logging.DEBUG, logArgs=False,
                 logTraceback=False):
  """ Returns a closure suitable for use as function/method decorator for
  logging entry/exit of function/method.

  getLoggerCallback:    user-supplied callback function that takes no args and
                          returns the logger instance to use for logging.
  entryExitLogLevel:    Log level for logging entry/exit of decorated function;
                          e.g., logging.DEBUG; pass None to disable entry/exit
                          logging.
  logArgs:              If True, also log args
  logTraceback:         If True, also log Traceback information

  Usage Examples:
    NOTE: logging must be initialized *before* any loggers are created, else
      there will be no output; see nupic.support.initLogging()

    @logEntryExit()
    def myFunctionBar():
        ...


    @logEntryExit(logTraceback=True)
    @logExceptions()
    def myFunctionGamma():
        ...
        raise RuntimeError("something bad happened")
        ...
  """

  def entryExitLoggingDecorator(func):

    @functools.wraps(func)
    def entryExitLoggingWrap(*args, **kwargs):

      if entryExitLogLevel is None:
        enabled = False
      else:
        logger = getLoggerCallback()
        enabled = logger.isEnabledFor(entryExitLogLevel)

      if not enabled:
        return func(*args, **kwargs)

      funcName = str(func)

      if logArgs:
        argsRepr = ', '.join(
          [repr(a) for a in args] +
          ['%s=%r' % (k,v,) for k,v in kwargs.iteritems()])
      else:
        argsRepr = ''

      logger.log(
        entryExitLogLevel, "ENTERING: %s(%s)%s", funcName, argsRepr,
        '' if not logTraceback else '; ' + repr(traceback.format_stack()))

      try:
        return func(*args, **kwargs)
      finally:
        logger.log(
          entryExitLogLevel, "LEAVING: %s(%s)%s", funcName, argsRepr,
          '' if not logTraceback else '; ' + repr(traceback.format_stack()))


    return entryExitLoggingWrap

  return entryExitLoggingDecorator