def run(command, parser, cl_args, unknown_args):
  """ run command """
  location = cl_args['cluster/[role]/[env]'].split('/')
  if len(location) == 1:
    return show_cluster(cl_args, *location)
  elif len(location) == 2:
    return show_cluster_role(cl_args, *location)
  elif len(location) == 3:
    return show_cluster_role_env(cl_args, *location)
  else:
    Log.error('Invalid topologies selection')
    return False