def create_parser(subparsers):
  """ Create the parse for the update command """
  parser = subparsers.add_parser(
      'update',
      help='Update a topology',
      usage="%(prog)s [options] cluster/[role]/[env] <topology-name> "
      + "[--component-parallelism <name:value>] "
      + "[--container-number value] "
      + "[--runtime-config [component:]<name:value>]",
      add_help=True)

  args.add_titles(parser)
  args.add_cluster_role_env(parser)
  args.add_topology(parser)

  args.add_config(parser)
  args.add_dry_run(parser)
  args.add_service_url(parser)
  args.add_verbose(parser)

  # Special parameters for update command
  def parallelism_type(value):
    pattern = re.compile(r"^[\w\.-]+:[\d]+$")
    if not pattern.match(value):
      raise argparse.ArgumentTypeError(
          "Invalid syntax for component parallelism (<component_name:value>): %s" % value)
    return value

  parser.add_argument(
      '--component-parallelism',
      action='append',
      type=parallelism_type,
      required=False,
      help='Component name and the new parallelism value '
      + 'colon-delimited: <component_name>:<parallelism>')

  def runtime_config_type(value):
    pattern = re.compile(r"^([\w\.-]+:){1,2}[\w\.-]+$")
    if not pattern.match(value):
      raise argparse.ArgumentTypeError(
          "Invalid syntax for runtime config ([component:]<name:value>): %s"
          % value)
    return value

  parser.add_argument(
      '--runtime-config',
      action='append',
      type=runtime_config_type,
      required=False,
      help='Runtime configurations for topology and components '
      + 'colon-delimited: [component:]<name>:<value>')

  def container_number_type(value):
    pattern = re.compile(r"^\d+$")
    if not pattern.match(value):
      raise argparse.ArgumentTypeError(
          "Invalid syntax for container number (value): %s"
          % value)
    return value

  parser.add_argument(
      '--container-number',
      action='append',
      type=container_number_type,
      required=False,
      help='Number of containers <value>')

  parser.set_defaults(subcommand='update')
  return parser