def show_cluster(cl_args, cluster):
  ''' print topologies information to stdout '''
  try:
    result = tracker_access.get_cluster_topologies(cluster)
    if not result:
      Log.error('No topologies in cluster \'%s\'' % cluster)
      return False
    result = result[cluster]
  except Exception:
    Log.error("Fail to connect to tracker: \'%s\'", cl_args["tracker_url"])
    return False
  table, header, rest_count = to_table(result)
  print('Topologies running in cluster \'%s\'' % cluster)
  if rest_count:
    print('  with %d more...' % rest_count)
  print(tabulate(table, headers=header))
  return True