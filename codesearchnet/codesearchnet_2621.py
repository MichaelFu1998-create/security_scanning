def get_all_zk_state_managers(conf):
  """
  Creates all the zookeeper state_managers and returns
  them in a list
  """
  state_managers = []
  state_locations = conf.get_state_locations_of_type("zookeeper")
  for location in state_locations:
    name = location['name']
    hostport = location['hostport']
    hostportlist = []
    for hostportpair in hostport.split(','):
      host = None
      port = None
      if ':' in hostport:
        hostandport = hostportpair.split(':')
        if len(hostandport) == 2:
          host = hostandport[0]
          port = int(hostandport[1])
      if not host or not port:
        raise Exception("Hostport for %s must be of the format 'host:port'." % (name))
      hostportlist.append((host, port))
    tunnelhost = location['tunnelhost']
    rootpath = location['rootpath']
    LOG.info("Connecting to zk hostports: " + str(hostportlist) + " rootpath: " + rootpath)
    state_manager = ZkStateManager(name, hostportlist, rootpath, tunnelhost)
    state_managers.append(state_manager)

  return state_managers