def create_parser(subparsers):
  '''
  :param subparsers:
  :return:
  '''
  parser = subparsers.add_parser(
      'config',
      help='Config properties for a cluster',
      usage="%(prog)s [cluster]",
      add_help=True)

  parser.add_argument(
      'cluster',
      help='Cluster to configure'
  )

  ex_subparsers = parser.add_subparsers(
      title="Commands",
      description=None)

  # add config list parser
  list_parser = ex_subparsers.add_parser(
      'list',
      help='List config properties for a cluster',
      usage="%(prog)s",
      add_help=True)
  list_parser.set_defaults(configcommand='list')

  # add config set parser
  set_parser = ex_subparsers.add_parser(
      'set',
      help='Set a cluster config property',
      usage="%(prog)s [property] [value]",
      add_help=True)

  set_parser.add_argument(
      'property',
      help='Config property to set'
  )

  set_parser.add_argument(
      'value',
      help='Value of config property'
  )
  set_parser.set_defaults(configcommand='set')

  # add config unset parser
  unset_parser = ex_subparsers.add_parser(
      'unset',
      help='Unset a cluster config property',
      usage="%(prog)s [property]",
      add_help=True)

  unset_parser.add_argument(
      'property',
      help='Config property to unset'
  )
  unset_parser.set_defaults(configcommand='unset')

  parser.set_defaults(subcommand='config')
  return parser