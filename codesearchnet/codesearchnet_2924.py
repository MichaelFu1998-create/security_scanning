def add_arguments(parser):
  """ add arguments """
  default_config_file = os.path.join(
      utils.get_heron_tracker_conf_dir(), constants.DEFAULT_CONFIG_FILE)

  parser.add_argument(
      '--config-file',
      metavar='(a string; path to config file; default: "' + default_config_file + '")',
      default=default_config_file)

  parser.add_argument(
      '--type',
      metavar='(an string; type of state manager (zookeeper or file, etc.); example: ' \
        + str(constants.DEFAULT_STATE_MANAGER_TYPE) + ')',
      choices=["file", "zookeeper"])

  parser.add_argument(
      '--name',
      metavar='(an string; name to be used for the state manager; example: ' \
        + str(constants.DEFAULT_STATE_MANAGER_NAME) + ')')

  parser.add_argument(
      '--rootpath',
      metavar='(an string; where all the states are stored; example: ' \
        + str(constants.DEFAULT_STATE_MANAGER_ROOTPATH) + ')')

  parser.add_argument(
      '--tunnelhost',
      metavar='(an string; if ssh tunneling needs to be established to connect to it; example: ' \
        + str(constants.DEFAULT_STATE_MANAGER_TUNNELHOST) + ')')

  parser.add_argument(
      '--hostport',
      metavar='(an string; only used to connect to zk, must be of the form \'host:port\';'\
      ' example: ' + str(constants.DEFAULT_STATE_MANAGER_HOSTPORT) + ')')

  parser.add_argument(
      '--port',
      metavar='(an integer; port to listen; default: ' + str(constants.DEFAULT_PORT) + ')',
      type=int,
      default=constants.DEFAULT_PORT)

  parser.add_argument(
      '--verbose',
      action='store_true')

  return parser