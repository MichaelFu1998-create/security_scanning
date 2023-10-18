def server_mode_cluster_role_env(cluster_role_env, config_map):
  """Check cluster/[role]/[environ], if they are required"""

  cmap = config_map[cluster_role_env[0]]

  # if role is required but not provided, raise exception
  role_present = True if len(cluster_role_env[1]) > 0 else False
  if ROLE_KEY in cmap and cmap[ROLE_KEY] and not role_present:
    raise Exception("role required but not provided (cluster/role/env = %s)."\
        % (cluster_role_env))

  # if environ is required but not provided, raise exception
  environ_present = True if len(cluster_role_env[2]) > 0 else False
  if ENVIRON_KEY in cmap and cmap[ENVIRON_KEY] and not environ_present:
    raise Exception("environ required but not provided (cluster/role/env = %s)."\
        % (cluster_role_env))

  return True