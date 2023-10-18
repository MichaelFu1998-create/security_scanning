def create_parser(subparsers):
  """ create parser """
  parser = subparsers.add_parser(
      'version',
      help='Display version',
      usage="%(prog)s",
      add_help=False)
  args.add_titles(parser)
  parser.set_defaults(subcommand='version')
  return parser