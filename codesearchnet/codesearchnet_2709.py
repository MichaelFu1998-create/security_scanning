def create_parser(subparsers):
  '''
  :param subparsers:
  :return:
  '''
  parser = subparsers.add_parser(
      'help',
      help='Prints help for commands',
      add_help=True)

  # pylint: disable=protected-access
  parser._positionals.title = "Required arguments"
  parser._optionals.title = "Optional arguments"

  parser.add_argument(
      'help-command',
      nargs='?',
      default='help',
      help='Provide help for a command')

  parser.set_defaults(subcommand='help')
  return parser