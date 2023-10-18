def run_containers(command, parser, cl_args, unknown_args):
  """ run containers subcommand """
  cluster, role, env = cl_args['cluster'], cl_args['role'], cl_args['environ']
  topology = cl_args['topology-name']
  container_id = cl_args['id']
  try:
    result = tracker_access.get_topology_info(cluster, env, topology, role)
  except:
    Log.error("Fail to connect to tracker: \'%s\'", cl_args["tracker_url"])
    return False
  containers = result['physical_plan']['stmgrs']
  all_bolts, all_spouts = set(), set()
  for _, bolts in result['physical_plan']['bolts'].items():
    all_bolts = all_bolts | set(bolts)
  for _, spouts in result['physical_plan']['spouts'].items():
    all_spouts = all_spouts | set(spouts)
  stmgrs = containers.keys()
  stmgrs.sort()
  if container_id is not None:
    try:
      normalized_cid = container_id - 1
      if normalized_cid < 0:
        raise
      stmgrs = [stmgrs[normalized_cid]]
    except:
      Log.error('Invalid container id: %d' % container_id)
      return False
  table = []
  for sid, name in enumerate(stmgrs):
    cid = sid + 1
    host = containers[name]["host"]
    port = containers[name]["port"]
    pid = containers[name]["pid"]
    instances = containers[name]["instance_ids"]
    bolt_nums = len([instance for instance in instances if instance in all_bolts])
    spout_nums = len([instance for instance in instances if instance in all_spouts])
    table.append([cid, host, port, pid, bolt_nums, spout_nums, len(instances)])
  headers = ["container", "host", "port", "pid", "#bolt", "#spout", "#instance"]
  sys.stdout.flush()
  print(tabulate(table, headers=headers))
  return True