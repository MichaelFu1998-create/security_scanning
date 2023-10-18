def create_parser(subparsers):
  """ create parser """
  metrics_parser = subparsers.add_parser(
      'metrics',
      help='Display info of a topology\'s metrics',
      usage="%(prog)s cluster/[role]/[env] topology-name [options]",
      add_help=False)
  args.add_cluster_role_env(metrics_parser)
  args.add_topology_name(metrics_parser)
  args.add_verbose(metrics_parser)
  args.add_tracker_url(metrics_parser)
  args.add_config(metrics_parser)
  args.add_component_name(metrics_parser)
  metrics_parser.set_defaults(subcommand='metrics')

  containers_parser = subparsers.add_parser(
      'containers',
      help='Display info of a topology\'s containers metrics',
      usage="%(prog)s cluster/[role]/[env] topology-name [options]",
      add_help=False)
  args.add_cluster_role_env(containers_parser)
  args.add_topology_name(containers_parser)
  args.add_verbose(containers_parser)
  args.add_tracker_url(containers_parser)
  args.add_config(containers_parser)
  args.add_container_id(containers_parser)
  containers_parser.set_defaults(subcommand='containers')

  return subparsers