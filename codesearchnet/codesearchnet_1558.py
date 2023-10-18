def _reportCommandLineUsageErrorAndExit(parser, message):
  """Report usage error and exit program with error indication."""
  print parser.get_usage()
  print message
  sys.exit(1)