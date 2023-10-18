def direct_mode_cluster_role_env(cluster_role_env, config_path):
  """Check cluster/[role]/[environ], if they are required"""

  # otherwise, get the client.yaml file
  cli_conf_file = os.path.join(config_path, CLIENT_YAML)

  # if client conf doesn't exist, use default value
  if not os.path.isfile(cli_conf_file):
    return True

  client_confs = {}
  with open(cli_conf_file, 'r') as conf_file:
    client_confs = yaml.load(conf_file)

    # the return value of yaml.load can be None if conf_file is an empty file
    if not client_confs:
      return True

    # if role is required but not provided, raise exception
    role_present = True if len(cluster_role_env[1]) > 0 else False
    if ROLE_REQUIRED in client_confs and client_confs[ROLE_REQUIRED] and not role_present:
      raise Exception("role required but not provided (cluster/role/env = %s). See %s in %s"
                      % (cluster_role_env, ROLE_REQUIRED, cli_conf_file))

    # if environ is required but not provided, raise exception
    environ_present = True if len(cluster_role_env[2]) > 0 else False
    if ENV_REQUIRED in client_confs and client_confs[ENV_REQUIRED] and not environ_present:
      raise Exception("environ required but not provided (cluster/role/env = %s). See %s in %s"
                      % (cluster_role_env, ENV_REQUIRED, cli_conf_file))

  return True