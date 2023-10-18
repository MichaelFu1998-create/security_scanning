def server_deployment_mode(command, parser, cluster, cl_args):
  '''
  check the server deployment mode for the given cluster
  if it is valid return the valid set of args
  :param cluster:
  :param cl_args:
  :return:
  '''
  # Read the cluster definition, if not found
  client_confs = cdefs.read_server_mode_cluster_definition(cluster, cl_args)

  if not client_confs[cluster]:
    return dict()

  # tell the user which definition that we are using
  if not cl_args.get('service_url', None):
    Log.debug("Using cluster definition from file %s" \
        % cliconfig.get_cluster_config_file(cluster))
  else:
    Log.debug("Using cluster service url %s" % cl_args['service_url'])

  # if cluster definition exists, but service_url is not set, it is an error
  if not 'service_url' in client_confs[cluster]:
    config_file = cliconfig.get_cluster_config_file(cluster)
    Log.error('No service url for %s cluster in %s', cluster, config_file)
    sys.exit(1)

  # get overrides
  if 'config_property' in cl_args:
    pass

  try:
    cluster_role_env = (cl_args['cluster'], cl_args['role'], cl_args['environ'])
    config.server_mode_cluster_role_env(cluster_role_env, client_confs)
    cluster_tuple = config.defaults_cluster_role_env(cluster_role_env)
  except Exception as ex:
    Log.error("Argument cluster/[role]/[env] is not correct: %s", str(ex))
    sys.exit(1)

  new_cl_args = dict()
  new_cl_args['cluster'] = cluster_tuple[0]
  new_cl_args['role'] = cluster_tuple[1]
  new_cl_args['environ'] = cluster_tuple[2]
  new_cl_args['service_url'] = client_confs[cluster]['service_url'].rstrip('/')
  new_cl_args['deploy_mode'] = config.SERVER_MODE

  cl_args.update(new_cl_args)
  return cl_args