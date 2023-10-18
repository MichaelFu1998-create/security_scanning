def initLogging(verbose=False, console='stdout', consoleLevel='DEBUG'):
  """
  Initilize NuPic logging by reading in from the logging configuration file. The
  logging configuration file is named ``nupic-logging.conf`` and is expected to
  be in the format defined by the python logging module.

  If the environment variable ``NTA_CONF_PATH`` is defined, then the logging
  configuration file is expected to be in the ``NTA_CONF_PATH`` directory. If
  ``NTA_CONF_PATH`` is not defined, then it is found in the 'conf/default'
  subdirectory of the NuPic installation directory (typically
  ~/nupic/current/conf/default)

  The logging configuration file can use the environment variable
  ``NTA_LOG_DIR`` to set the locations of log files. If this variable is not
  defined, logging to files will be disabled.

  :param console: Defines console output for the default "root" logging
              configuration; this may be one of 'stdout', 'stderr', or None;
              Use None to suppress console logging output
  :param consoleLevel:
              Logging-level filter string for console output corresponding to
              logging levels in the logging module; may be one of:
              'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'.
              E.g.,  a value of'WARNING' suppresses DEBUG and INFO level output
              to console, but allows WARNING, ERROR, and CRITICAL
  """

  # NOTE: If you call this twice from the same process there seems to be a
  # bug - logged messages don't show up for loggers that you do another
  # logging.getLogger() on.
  global gLoggingInitialized
  if gLoggingInitialized:
    if verbose:
      print >> sys.stderr, "Logging already initialized, doing nothing."
    return

  consoleStreamMappings = {
    'stdout'  : 'stdoutConsoleHandler',
    'stderr'  : 'stderrConsoleHandler',
  }

  consoleLogLevels = ['DEBUG', 'INFO', 'WARNING', 'WARN', 'ERROR', 'CRITICAL',
                      'FATAL']

  assert console is None or console in consoleStreamMappings.keys(), (
    'Unexpected console arg value: %r') % (console,)

  assert consoleLevel in consoleLogLevels, (
    'Unexpected consoleLevel arg value: %r') % (consoleLevel)

  # -----------------------------------------------------------------------
  # Setup logging. Look for the nupic-logging.conf file, first in the
  #   NTA_CONFIG_DIR path (if defined), then in a subdirectory of the nupic
  #   module
  configFilename = 'nupic-logging.conf'
  configFilePath = resource_filename("nupic.support", configFilename)

  configLogDir = os.environ.get('NTA_LOG_DIR', None)

  # Load in the logging configuration file
  if verbose:
    print >> sys.stderr, (
      "Using logging configuration file: %s") % (configFilePath)

  # This dict will hold our replacement strings for logging configuration
  replacements = dict()

  def makeKey(name):
    """ Makes replacement key """
    return "$$%s$$" % (name)

  platform = sys.platform.lower()
  if platform.startswith('java'):
    # Jython
    import java.lang
    platform = java.lang.System.getProperty("os.name").lower()
    if platform.startswith('mac os x'):
      platform = 'darwin'

  if platform.startswith('darwin'):
    replacements[makeKey('SYSLOG_HANDLER_ADDRESS')] = '"/var/run/syslog"'
  elif platform.startswith('linux'):
    replacements[makeKey('SYSLOG_HANDLER_ADDRESS')] = '"/dev/log"'
  elif platform.startswith('win'):
    replacements[makeKey('SYSLOG_HANDLER_ADDRESS')] = '"log"'
  else:
    raise RuntimeError("This platform is neither darwin, win32, nor linux: %s" % (
      sys.platform,))

  # Nupic logs go to file
  replacements[makeKey('PERSISTENT_LOG_HANDLER')] = 'fileHandler'
  if platform.startswith('win'):
    replacements[makeKey('FILE_HANDLER_LOG_FILENAME')] = '"NUL"'
  else:
    replacements[makeKey('FILE_HANDLER_LOG_FILENAME')] = '"/dev/null"'

  # Set up log file path for the default file handler and configure handlers
  handlers = list()

  if configLogDir is not None:
    logFilePath = _genLoggingFilePath()
    makeDirectoryFromAbsolutePath(os.path.dirname(logFilePath))
    replacements[makeKey('FILE_HANDLER_LOG_FILENAME')] = repr(logFilePath)

    handlers.append(replacements[makeKey('PERSISTENT_LOG_HANDLER')])

  if console is not None:
    handlers.append(consoleStreamMappings[console])

  replacements[makeKey('ROOT_LOGGER_HANDLERS')] = ", ".join(handlers)

  # Set up log level for console handlers
  replacements[makeKey('CONSOLE_LOG_LEVEL')] = consoleLevel

  customConfig = StringIO()

  # Using pkg_resources to get the logging file, which should be packaged and
  # associated with this source file name.
  loggingFileContents = resource_string(__name__, configFilename)

  for lineNum, line in enumerate(loggingFileContents.splitlines()):
    if "$$" in line:
      for (key, value) in replacements.items():
        line = line.replace(key, value)

    # If there is still a replacement string in the line, we're missing it
    #  from our replacements dict
    if "$$" in line and "$$<key>$$" not in line:
      raise RuntimeError(("The text %r, found at line #%d of file %r, "
                          "contains a string not found in our replacement "
                          "dict.") % (line, lineNum, configFilePath))

    customConfig.write("%s\n" % line)

  customConfig.seek(0)
  if python_version()[:3] >= '2.6':
    logging.config.fileConfig(customConfig, disable_existing_loggers=False)
  else:
    logging.config.fileConfig(customConfig)

  gLoggingInitialized = True