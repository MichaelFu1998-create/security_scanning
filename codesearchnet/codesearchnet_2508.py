def run(command, parser, args, unknown_args):
  """ run command """
  # get the command for detailed help
  command_help = args['help-command']

  # if no command is provided, just print main help
  if command_help == 'help':
    parser.print_help()
    return True

  # get the subparser for the specific command
  subparser = config.get_subparser(parser, command_help)
  if subparser:
    print(subparser.format_help())
    return True
  else:
    Log.error("Unknown subcommand \'%s\'" % command_help)
    return False