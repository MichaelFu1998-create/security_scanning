def start_cluster(cl_args):
  '''
  Start a Heron standalone cluster
  '''
  roles = read_and_parse_roles(cl_args)
  masters = roles[Role.MASTERS]
  slaves = roles[Role.SLAVES]
  zookeepers = roles[Role.ZOOKEEPERS]
  Log.info("Roles:")
  Log.info(" - Master Servers: %s" % list(masters))
  Log.info(" - Slave Servers: %s" % list(slaves))
  Log.info(" - Zookeeper Servers: %s" % list(zookeepers))
  if not masters:
    Log.error("No master servers specified!")
    sys.exit(-1)
  if not slaves:
    Log.error("No slave servers specified!")
    sys.exit(-1)
  if not zookeepers:
    Log.error("No zookeeper servers specified!")
    sys.exit(-1)
  # make sure configs are templated
  update_config_files(cl_args)

  dist_nodes = list(masters.union(slaves))
  # if just local deployment
  if not (len(dist_nodes) == 1 and is_self(dist_nodes[0])):
    distribute_package(roles, cl_args)
  start_master_nodes(masters, cl_args)
  start_slave_nodes(slaves, cl_args)
  start_api_server(masters, cl_args)
  start_heron_tools(masters, cl_args)
  Log.info("Heron standalone cluster complete!")