def load_state_manager_locations(cluster, state_manager_config_file='heron-conf/statemgr.yaml',
                                 overrides={}):
  """ Reads configs to determine which state manager to use and converts them to state manager
  locations. Handles a subset of config wildcard substitution supported in the substitute method in
  org.apache.heron.spi.common.Misc.java"""
  with open(state_manager_config_file, 'r') as stream:
    config = yaml.load(stream)

  home_dir = os.path.expanduser("~")
  wildcards = {
      "~" : home_dir,
      "${HOME}" : home_dir,
      "${CLUSTER}" : cluster,
  }
  if os.getenv('JAVA_HOME'):
    wildcards["${JAVA_HOME}"] = os.getenv('JAVA_HOME')

  config = __replace(config, wildcards, state_manager_config_file)

  # merge with overrides
  if overrides:
    config.update(overrides)

  # need to convert from the format in statemgr.yaml to the format that the python state managers
  # takes. first, set reasonable defaults to local
  state_manager_location = {
      'type': 'file',
      'name': 'local',
      'tunnelhost': '127.0.0.1',
      'rootpath': '~/.herondata/repository/state/local',
  }

  # then map the statemgr.yaml config keys to the python state manager location
  key_mappings = {
      'heron.statemgr.connection.string': 'hostport',
      'heron.statemgr.tunnel.host': 'tunnelhost',
      'heron.statemgr.root.path': 'rootpath',
  }
  for config_key in key_mappings:
    if config_key in config:
      state_manager_location[key_mappings[config_key]] = config[config_key]

  state_manager_class = config['heron.class.state.manager']
  if state_manager_class == 'org.apache.heron.statemgr.zookeeper.curator.CuratorStateManager':
    state_manager_location['type'] = 'zookeeper'
    state_manager_location['name'] = 'zk'

  return [state_manager_location]