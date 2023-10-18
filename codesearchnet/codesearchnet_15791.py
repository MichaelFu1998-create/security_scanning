def validate_arguments(args):
  """
  Validate that the necessary argument for normal or diff analysis are specified.
  :param: args: Command line arguments namespace
  """
  if args.diff:
    if not args.output_dir:
      logger.error('No Output location specified')
      print_usage()
      sys.exit(0)
  # elif not (args.config and args.output_dir):
  elif not args.output_dir:
    print_usage()
    sys.exit(0)