def direct_deployment_mode(command, parser, cluster, cl_args):
  '''
  check the direct deployment mode for the given cluster
  if it is valid return the valid set of args
  :param command:
  :param parser:
  :param cluster:
  :param cl_args:
  :return:
  '''

  cluster = cl_args['cluster']
  try:
    config_path = cl_args['config_path']
    override_config_file = config.parse_override_config_and_write_file(cl_args['config_property'])
  except KeyError:
    # if some of the arguments are not found, print error and exit
    subparser = config.get_subparser(parser, command)
    print(subparser.format_help())
    return dict()

  # check if the cluster config directory exists
  if not cdefs.check_direct_mode_cluster_definition(cluster, config_path):
    Log.error("Cluster config directory \'%s\' does not exist", config_path)
    return dict()

  config_path = config.get_heron_cluster_conf_dir(cluster, config_path)
  if not os.path.isdir(config_path):
    Log.error("Cluster config directory \'%s\' does not exist", config_path)
    return dict()

  Log.info("Using cluster definition in %s" % config_path)

  try:
    cluster_role_env = (cl_args['cluster'], cl_args['role'], cl_args['environ'])
    config.direct_mode_cluster_role_env(cluster_role_env, config_path)
    cluster_tuple = config.defaults_cluster_role_env(cluster_role_env)
  except Exception as ex:
    Log.error("Argument cluster/[role]/[env] is not correct: %s", str(ex))
    return dict()

  new_cl_args = dict()
  new_cl_args['cluster'] = cluster_tuple[0]
  new_cl_args['role'] = cluster_tuple[1]
  new_cl_args['environ'] = cluster_tuple[2]
  new_cl_args['config_path'] = config_path
  new_cl_args['override_config_file'] = override_config_file
  new_cl_args['deploy_mode'] = config.DIRECT_MODE

  cl_args.update(new_cl_args)
  return cl_args