def create_parser(command_handlers):
  '''
  Main parser
  :return:
  '''
  parser = argparse.ArgumentParser(
      prog='heron',
      epilog=HELP_EPILOG,
      formatter_class=config.SubcommandHelpFormatter,
      add_help=True)

  subparsers = parser.add_subparsers(
      title="Available commands",
      metavar='<command> <options>')

  command_list = sorted(command_handlers.items())
  for command in command_list:
    command[1].create_parser(subparsers)

  return parser