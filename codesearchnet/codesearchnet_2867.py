def parse_config_file(config_file):
  """
  This will parse the config file for the tracker
  :return: the config or None if the file is not found
  """
  expanded_config_file_path = os.path.expanduser(config_file)
  if not os.path.lexists(expanded_config_file_path):
    return None

  configs = {}
  # Read the configuration file
  with open(expanded_config_file_path, 'r') as f:
    configs = yaml.load(f)

  return configs