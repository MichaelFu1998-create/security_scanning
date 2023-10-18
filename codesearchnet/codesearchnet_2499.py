def defaults_cluster_role_env(cluster_role_env):
  """
  if role is not provided, supply userid
  if environ is not provided, supply 'default'
  """
  if len(cluster_role_env[1]) == 0 and len(cluster_role_env[2]) == 0:
    return (cluster_role_env[0], getpass.getuser(), ENVIRON)

  return (cluster_role_env[0], cluster_role_env[1], cluster_role_env[2])