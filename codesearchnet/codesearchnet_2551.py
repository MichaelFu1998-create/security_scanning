def run(cl_args, compo_type):
  """ run command """
  cluster, role, env = cl_args['cluster'], cl_args['role'], cl_args['environ']
  topology = cl_args['topology-name']
  spouts_only, bolts_only = cl_args['spout'], cl_args['bolt']
  try:
    components = tracker_access.get_logical_plan(cluster, env, topology, role)
    topo_info = tracker_access.get_topology_info(cluster, env, topology, role)
    table, header = to_table(components, topo_info)
    if spouts_only == bolts_only:
      print(tabulate(table, headers=header))
    elif spouts_only:
      table, header = filter_spouts(table, header)
      print(tabulate(table, headers=header))
    else:
      table, header = filter_bolts(table, header)
      print(tabulate(table, headers=header))
    return True
  except:
    Log.error("Fail to connect to tracker: \'%s\'", cl_args["tracker_url"])
    return False