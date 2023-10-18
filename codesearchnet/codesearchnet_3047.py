def extract_common_args(command, parser, cl_args):
  """ extract common args """
  try:
    # do not pop like cli because ``topologies`` subcommand still needs it
    cluster_role_env = cl_args['cluster/[role]/[env]']
    config_path = cl_args['config_path']
  except KeyError:
    # if some of the arguments are not found, print error and exit
    subparser = config.get_subparser(parser, command)
    print(subparser.format_help())
    return dict()
  cluster = config.get_heron_cluster(cluster_role_env)
  config_path = config.get_heron_cluster_conf_dir(cluster, config_path)

  new_cl_args = dict()
  try:
    cluster_tuple = config.parse_cluster_role_env(cluster_role_env, config_path)
    new_cl_args['cluster'] = cluster_tuple[0]
    new_cl_args['role'] = cluster_tuple[1]
    new_cl_args['environ'] = cluster_tuple[2]
    new_cl_args['config_path'] = config_path
  except Exception as e:
    Log.error("Unable to get valid topology location: %s", str(e))
    return dict()

  cl_args.update(new_cl_args)
  return cl_args