def print_cluster_info(cl_args):
  '''
  get cluster info for standalone cluster
  '''
  parsed_roles = read_and_parse_roles(cl_args)
  masters = list(parsed_roles[Role.MASTERS])
  slaves = list(parsed_roles[Role.SLAVES])
  zookeepers = list(parsed_roles[Role.ZOOKEEPERS])
  cluster = list(parsed_roles[Role.CLUSTER])

  # OrderedDicts are used here so that the key order can be
  # specified directly
  info = OrderedDict()
  info['numNodes'] = len(cluster)
  info['nodes'] = cluster
  roles = OrderedDict()
  roles['masters'] = masters
  roles['slaves'] = slaves
  roles['zookeepers'] = zookeepers
  urls = OrderedDict()
  urls['serviceUrl'] = get_service_url(cl_args)
  urls['heronUi'] = get_heron_ui_url(cl_args)
  urls['heronTracker'] = get_heron_tracker_url(cl_args)
  info['roles'] = roles
  info['urls'] = urls

  print json.dumps(info, indent=2)