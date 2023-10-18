def get_cluster_role_env_topologies(cluster, role, env):
  '''
  Get the list of topologies given a cluster submitted by a given role under a given environment
  :param cluster:
  :param role:
  :param env:
  :return:
  '''
  return _get_topologies(cluster, role=role, env=env)