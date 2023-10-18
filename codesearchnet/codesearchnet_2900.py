def check_direct_mode_cluster_definition(cluster, config_path):
  '''
  Check the cluster definition for direct mode
  :param cluster:
  :param config_path:
  :return:
  '''
  config_path = config.get_heron_cluster_conf_dir(cluster, config_path)
  if not os.path.isdir(config_path):
    return False
  return True