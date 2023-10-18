def add_config(parser):
  """ add config """
  # the default config path
  default_config_path = config.get_heron_conf_dir()

  parser.add_argument(
      '--config-path',
      metavar='(a string; path to cluster config; default: "' + default_config_path + '")',
      default=os.path.join(config.get_heron_dir(), default_config_path))

  return parser