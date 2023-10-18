def execute(handlers, local_commands):
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
  is_local_command = command in local_commands

  if command == 'version':
    results = run(handlers, command, parser, command_line_args, unknown_args)
    return 0 if result.is_successful(results) else 1

  if not is_local_command:
    log.set_logging_level(command_line_args)
    Log.debug("Input Command Line Args: %s", command_line_args)

    # determine the mode of deployment
    command_line_args = extract_common_args(command, parser, command_line_args)
    command_line_args = deployment_mode(command, parser, command_line_args)

    # bail out if args are empty
    if not command_line_args:
      return 1

    # register dirs cleanup function during exit
    if command_line_args['deploy_mode'] == config.DIRECT_MODE and command != "version":
      cleaned_up_files.append(command_line_args['override_config_file'])
      atexit.register(cleanup, cleaned_up_files)

  # print the input parameters, if verbose is enabled
  Log.debug("Processed Command Line Args: %s", command_line_args)

  start = time.time()
  results = run(handlers, command, parser, command_line_args, unknown_args)
  if not is_local_command:
    result.render(results)
  end = time.time()

  if not is_local_command:
    sys.stdout.flush()
    Log.debug('Elapsed time: %.3fs.', (end - start))

  return 0 if result.is_successful(results) else 1