def read_server_mode_cluster_definition(cluster, cl_args):
  '''
  Read the cluster definition for server mode
  :param cluster:
  :param cl_args:
  :param config_file:
  :return:
  '''

  client_confs = dict()
  client_confs[cluster] = cliconfig.cluster_config(cluster)

  # now check if the service-url from command line is set, if so override it
  if cl_args.get('service_url', None):
    client_confs[cluster]['service_url'] = cl_args['service_url']

  # the return value of yaml.load can be None if conf_file is an empty file
  # or there is no service-url in command line, if needed.

  return client_confs