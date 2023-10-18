def parse_topo_loc(cl_args):
  """ parse topology location """
  try:
    topo_loc = cl_args['cluster/[role]/[env]'].split('/')
    topo_name = cl_args['topology-name']
    topo_loc.append(topo_name)
    if len(topo_loc) != 4:
      raise
    return topo_loc
  except Exception:
    Log.error('Invalid topology location')
    raise