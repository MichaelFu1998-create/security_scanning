def create_parser():
  """ create parser """
  help_epilog = '''Getting more help:
  heron-explorer help <command>     Disply help and options for <command>\n
  For detailed documentation, go to http://heronstreaming.io'''

  parser = argparse.ArgumentParser(
      prog='heron-explorer',
      epilog=help_epilog,
      formatter_class=SubcommandHelpFormatter,
      add_help=False)

  # sub-commands
  subparsers = parser.add_subparsers(
      title="Available commands",
      metavar='<command> <options>')

  # subparser for subcommands related to clusters
  clusters.create_parser(subparsers)

  # subparser for subcommands related to logical plan
  logicalplan.create_parser(subparsers)

  # subparser for subcommands related to physical plan
  physicalplan.create_parser(subparsers)

  # subparser for subcommands related to displaying info
  topologies.create_parser(subparsers)

  # subparser for help subcommand
  help.create_parser(subparsers)

  # subparser for version subcommand
  version.create_parser(subparsers)

  return parser