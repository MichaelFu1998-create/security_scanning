def get_cluster_role_env(cluster_role_env):
  """Parse cluster/[role]/[environ], supply empty string, if not provided"""
  parts = cluster_role_env.split('/')[:3]
  if len(parts) == 3:
    return (parts[0], parts[1], parts[2])

  if len(parts) == 2:
    return (parts[0], parts[1], "")

  if len(parts) == 1:
    return (parts[0], "", "")

  return ("", "", "")