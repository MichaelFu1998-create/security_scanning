def _genLoggingFilePath():
  """ Generate a filepath for the calling app """
  appName = os.path.splitext(os.path.basename(sys.argv[0]))[0] or 'UnknownApp'
  appLogDir = os.path.abspath(os.path.join(
    os.environ['NTA_LOG_DIR'],
    'numenta-logs-%s' % (os.environ['USER'],),
    appName))
  appLogFileName = '%s-%s-%s.log' % (
    appName, long(time.mktime(time.gmtime())), os.getpid())
  return os.path.join(appLogDir, appLogFileName)