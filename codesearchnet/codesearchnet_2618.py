def create_parser(subparsers, action, help_arg):
  '''
  :param subparsers:
  :param action:
  :param help_arg:
  :return:
  '''
  parser = subparsers.add_parser(
      action,
      help=help_arg,
      usage="%(prog)s [options] cluster/[role]/[env] <topology-name>",
      add_help=True)

  args.add_titles(parser)
  args.add_cluster_role_env(parser)
  args.add_topology(parser)

  args.add_config(parser)
  args.add_service_url(parser)
  args.add_verbose(parser)

  parser.set_defaults(subcommand=action)
  return parser