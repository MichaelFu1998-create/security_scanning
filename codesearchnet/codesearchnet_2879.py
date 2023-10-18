def yaml_config_reader(config_path):
  """Reads yaml config file and returns auto-typed config_dict"""
  if not config_path.endswith(".yaml"):
    raise ValueError("Config file not yaml")

  with open(config_path, 'r') as f:
    config = yaml.load(f)

  return config