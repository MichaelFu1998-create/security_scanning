def add_config(parser):
  '''
  :param parser:
  :return:
  '''
  # the default config path
  default_config_path = config.get_heron_conf_dir()

  parser.add_argument(
      '--config-path',
      default=os.path.join(config.get_heron_dir(), default_config_path),
      help='Path to cluster configuration files')

  parser.add_argument(
      '--config-property',
      metavar='PROPERTY=VALUE',
      action='append',
      default=[],
      help='Configuration properties that overrides default options')
  return parser