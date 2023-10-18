def create_parser(subparsers):
  """ create argument parser """
  parser = subparsers.add_parser(
      'clusters',
      help='Display existing clusters',
      usage="%(prog)s [options]",
      add_help=True)
  args.add_verbose(parser)
  args.add_tracker_url(parser)
  parser.set_defaults(subcommand='clusters')
  return subparsers