def create_parser(subparsers):
  """ create parser """
  components_parser = subparsers.add_parser(
      'components',
      help='Display information of a topology\'s components',
      usage="%(prog)s cluster/[role]/[env] topology-name [options]",
      add_help=False)
  args.add_cluster_role_env(components_parser)
  args.add_topology_name(components_parser)
  args.add_spouts(components_parser)
  args.add_bolts(components_parser)
  args.add_verbose(components_parser)
  args.add_tracker_url(components_parser)
  args.add_config(components_parser)
  components_parser.set_defaults(subcommand='components')

  return subparsers