def run(command, parser, args, unknown_args):
  '''
  :param command:
  :param parser:
  :param args:
  :param unknown_args:
  :return:
  '''
  # get the command for detailed help
  command_help = args['help-command']

  # if no command is provided, just print main help
  if command_help == 'help':
    parser.print_help()
    return SimpleResult(Status.Ok)

  # get the subparser for the specific command
  subparser = config.get_subparser(parser, command_help)
  if subparser:
    print(subparser.format_help())
    return SimpleResult(Status.Ok)
  else:
    Log.error("Unknown subcommand \'%s\'", command_help)
    return SimpleResult(Status.InvocationError)