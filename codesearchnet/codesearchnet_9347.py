def handle_version_flag():
  """If the --version flag is passed, print version to stdout and exit.

  Within dsub commands, --version should be the highest priority flag.
  This function supplies a repeatable and DRY way of checking for the
  version flag and printing the version. Callers still need to define a version
  flag in the command's flags so that it shows up in help output.
  """
  parser = argparse.ArgumentParser(description='Version parser', add_help=False)
  parser.add_argument('--version', '-v', dest='version', action='store_true')
  parser.set_defaults(version=False)
  args, _ = parser.parse_known_args()
  if args.version:
    print('dsub version: %s' % DSUB_VERSION)
    sys.exit()