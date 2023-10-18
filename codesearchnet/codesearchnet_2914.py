def run_metrics(command, parser, cl_args, unknown_args):
  """ run metrics subcommand """
  cluster, role, env = cl_args['cluster'], cl_args['role'], cl_args['environ']
  topology = cl_args['topology-name']
  try:
    result = tracker_access.get_topology_info(cluster, env, topology, role)
    spouts = result['physical_plan']['spouts'].keys()
    bolts = result['physical_plan']['bolts'].keys()
    components = spouts + bolts
    cname = cl_args['component']
    if cname:
      if cname in components:
        components = [cname]
      else:
        Log.error('Unknown component: \'%s\'' % cname)
        raise
  except Exception:
    Log.error("Fail to connect to tracker: \'%s\'", cl_args["tracker_url"])
    return False
  cresult = []
  for comp in components:
    try:
      metrics = tracker_access.get_component_metrics(comp, cluster, env, topology, role)
    except:
      Log.error("Fail to connect to tracker: \'%s\'", cl_args["tracker_url"])
      return False
    stat, header = to_table(metrics)
    cresult.append((comp, stat, header))
  for i, (comp, stat, header) in enumerate(cresult):
    if i != 0:
      print('')
    print('\'%s\' metrics:' % comp)
    print(tabulate(stat, headers=header))
  return True