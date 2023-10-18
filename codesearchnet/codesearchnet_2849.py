def create_parser(subparsers):
  '''
  Create a subparser for the submit command
  :param subparsers:
  :return:
  '''
  parser = subparsers.add_parser(
      'submit',
      help='Submit a topology',
      usage="%(prog)s [options] cluster/[role]/[env] " + \
            "topology-file-name topology-class-name [topology-args]",
      add_help=True
  )

  cli_args.add_titles(parser)
  cli_args.add_cluster_role_env(parser)
  cli_args.add_topology_file(parser)
  cli_args.add_topology_class(parser)
  cli_args.add_config(parser)
  cli_args.add_deactive_deploy(parser)
  cli_args.add_dry_run(parser)
  cli_args.add_extra_launch_classpath(parser)
  cli_args.add_release_yaml_file(parser)
  cli_args.add_service_url(parser)
  cli_args.add_system_property(parser)
  cli_args.add_verbose(parser)

  parser.set_defaults(subcommand='submit')
  return parser