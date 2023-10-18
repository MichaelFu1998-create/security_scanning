def parse_cluster_role_env(cluster_role_env, config_path):
  """Parse cluster/[role]/[environ], supply default, if not provided, not required"""
  parts = cluster_role_env.split('/')[:3]
  if not os.path.isdir(config_path):
    Log.error("Config path cluster directory does not exist: %s" % config_path)
    raise Exception("Invalid config path")

  # if cluster/role/env is not completely provided, check further
  if len(parts) < 3:

    cli_conf_file = os.path.join(config_path, CLIENT_YAML)

    # if client conf doesn't exist, use default value
    if not os.path.isfile(cli_conf_file):
      if len(parts) == 1:
        parts.append(getpass.getuser())
      if len(parts) == 2:
        parts.append(ENVIRON)
    else:
      cli_confs = {}
      with open(cli_conf_file, 'r') as conf_file:
        tmp_confs = yaml.load(conf_file)
        # the return value of yaml.load can be None if conf_file is an empty file
        if tmp_confs is not None:
          cli_confs = tmp_confs
        else:
          print("Failed to read: %s due to it is empty" % (CLIENT_YAML))

      # if role is required but not provided, raise exception
      if len(parts) == 1:
        if (ROLE_REQUIRED in cli_confs) and (cli_confs[ROLE_REQUIRED] is True):
          raise Exception("role required but not provided (cluster/role/env = %s). See %s in %s"
                          % (cluster_role_env, ROLE_REQUIRED, cli_conf_file))
        else:
          parts.append(getpass.getuser())

      # if environ is required but not provided, raise exception
      if len(parts) == 2:
        if (ENV_REQUIRED in cli_confs) and (cli_confs[ENV_REQUIRED] is True):
          raise Exception("environ required but not provided (cluster/role/env = %s). See %s in %s"
                          % (cluster_role_env, ENV_REQUIRED, cli_conf_file))
        else:
          parts.append(ENVIRON)

  # if cluster or role or environ is empty, print
  if len(parts[0]) == 0 or len(parts[1]) == 0 or len(parts[2]) == 0:
    print("Failed to parse")
    sys.exit(1)

  return (parts[0], parts[1], parts[2])