def show_cluster_role(cl_args, cluster, role):
  ''' print topologies information to stdout '''
  try:
    result = tracker_access.get_cluster_role_topologies(cluster, role)
    if not result:
      Log.error('Unknown cluster/role \'%s\'' % '/'.join([cluster, role]))
      return False
    result = result[cluster]
  except Exception:
    Log.error("Fail to connect to tracker: \'%s\'", cl_args["tracker_url"])
    return False
  table, header, rest_count = to_table(result)
  print('Topologies running in cluster \'%s\' submitted by \'%s\':' % (cluster, role))
  if rest_count:
    print('  with %d more...' % rest_count)
  print(tabulate(table, headers=header))
  return True