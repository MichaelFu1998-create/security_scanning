def execute(handlers):
  '''
  Run the command
  :return:
  '''
  # verify if the environment variables are correctly set
  check_environment()

  # create the argument parser
  parser = create_parser(handlers)

  # if no argument is provided, print help and exit
  if len(sys.argv[1:]) == 0:
    parser.print_help()
    return 0

  # insert the boolean values for some of the options
  sys.argv = config.insert_bool_values(sys.argv)

  try:
    # parse the args
    args, unknown_args = parser.parse_known_args()
  except ValueError as ex:
    Log.error("Error while parsing arguments: %s", str(ex))
    Log.debug(traceback.format_exc())
    sys.exit(1)

  command_line_args = vars(args)

  # set log level
  log.set_logging_level(command_line_args)
  Log.debug("Input Command Line Args: %s", command_line_args)

  # command to be execute
  command = command_line_args['subcommand']

  # print the input parameters, if verbose is enabled
  Log.debug("Processed Command Line Args: %s", command_line_args)

  results = run(handlers, command, parser, command_line_args, unknown_args)

  return 0 if result.is_successful(results) else 1