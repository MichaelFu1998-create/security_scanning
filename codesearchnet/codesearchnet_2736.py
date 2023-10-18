def read_and_parse_roles(cl_args):
  '''
  read config files to get roles
  '''
  roles = dict()

  with open(get_inventory_file(cl_args), 'r') as stream:
    try:
      roles = yaml.load(stream)
    except yaml.YAMLError as exc:
      Log.error("Error parsing inventory file: %s" % exc)
      sys.exit(-1)

  if Role.ZOOKEEPERS not in roles or not roles[Role.ZOOKEEPERS]:
    Log.error("Zookeeper servers node defined!")
    sys.exit(-1)

  if Role.CLUSTER not in roles or not roles[Role.CLUSTER]:
    Log.error("Heron cluster nodes defined!")
    sys.exit(-1)

  # Set roles
  roles[Role.MASTERS] = set([roles[Role.CLUSTER][0]])
  roles[Role.SLAVES] = set(roles[Role.CLUSTER])
  roles[Role.ZOOKEEPERS] = set(roles[Role.ZOOKEEPERS])
  roles[Role.CLUSTER] = set(roles[Role.CLUSTER])

  return roles