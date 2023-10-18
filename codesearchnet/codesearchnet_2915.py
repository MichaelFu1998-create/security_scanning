def run_bolts(command, parser, cl_args, unknown_args):
  """ run bolts subcommand """
  cluster, role, env = cl_args['cluster'], cl_args['role'], cl_args['environ']
  topology = cl_args['topology-name']
  try:
    result = tracker_access.get_topology_info(cluster, env, topology, role)
    bolts = result['physical_plan']['bolts'].keys()
    bolt_name = cl_args['bolt']
    if bolt_name:
      if bolt_name in bolts:
        bolts = [bolt_name]
      else:
        Log.error('Unknown bolt: \'%s\'' % bolt_name)
        raise
  except Exception:
    Log.error("Fail to connect to tracker: \'%s\'", cl_args["tracker_url"])
    return False
  bolts_result = []
  for bolt in bolts:
    try:
      metrics = tracker_access.get_component_metrics(bolt, cluster, env, topology, role)
      stat, header = to_table(metrics)
      bolts_result.append((bolt, stat, header))
    except Exception:
      Log.error("Fail to connect to tracker: \'%s\'", cl_args["tracker_url"])
      return False
  for i, (bolt, stat, header) in enumerate(bolts_result):
    if i != 0:
      print('')
    print('\'%s\' metrics:' % bolt)
    print(tabulate(stat, headers=header))
  return True