def main(args):
  """ main """
  # create the argument parser
  parser = create_parser()

  # if no argument is provided, print help and exit
  if not args:
    parser.print_help()
    return 0

  # insert the boolean values for some of the options
  all_args = parse.insert_bool_values(args)

  # parse the args
  args, unknown_args = parser.parse_known_args(args=all_args)
  command_line_args = vars(args)
  command = command_line_args['subcommand']

  if unknown_args:
    Log.error('Unknown argument: %s', unknown_args[0])
    # show help message
    command_line_args['help-command'] = command
    command = 'help'

  if command not in ['help', 'version']:
    opts.set_tracker_url(command_line_args)
    log.set_logging_level(command_line_args)
    if command not in ['topologies', 'clusters']:
      command_line_args = extract_common_args(command, parser, command_line_args)
    if not command_line_args:
      return 1
    Log.info("Using tracker URL: %s", command_line_args["tracker_url"])

  # timing command execution
  start = time.time()
  ret = run(command, parser, command_line_args, unknown_args)
  end = time.time()

  if command != 'help':
    sys.stdout.flush()
    Log.info('Elapsed time: %.3fs.', (end - start))

  return 0 if ret else 1