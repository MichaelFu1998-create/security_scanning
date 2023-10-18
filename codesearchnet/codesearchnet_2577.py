def create_parser(subparsers):
  '''
  :param subparsers:
  :return:
  '''
  parser = subparsers.add_parser(
      'version',
      help='Print version of heron-cli',
      usage="%(prog)s [options] [cluster]",
      add_help=True)

  add_version_titles(parser)

  parser.add_argument(
      'cluster',
      nargs='?',
      type=str,
      default="",
      help='Name of the cluster')

  cli_args.add_service_url(parser)

  parser.set_defaults(subcommand='version')
  return parser