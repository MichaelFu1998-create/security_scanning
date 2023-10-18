def extract_common_args(command, parser, cl_args):
  '''
  Extract all the common args for all commands
  :param command:
  :param parser:
  :param cl_args:
  :return:
  '''
  try:
    cluster_role_env = cl_args.pop('cluster/[role]/[env]')
  except KeyError:
    try:
      cluster_role_env = cl_args.pop('cluster')  # for version command
    except KeyError:
      # if some of the arguments are not found, print error and exit
      subparser = config.get_subparser(parser, command)
      print(subparser.format_help())
      return dict()

  new_cl_args = dict()
  cluster_tuple = config.get_cluster_role_env(cluster_role_env)
  new_cl_args['cluster'] = cluster_tuple[0]
  new_cl_args['role'] = cluster_tuple[1]
  new_cl_args['environ'] = cluster_tuple[2]
  new_cl_args['submit_user'] = getpass.getuser()

  cl_args.update(new_cl_args)
  return cl_args