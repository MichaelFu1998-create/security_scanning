def parse_override_config_and_write_file(namespace):
  """
  Parse the command line for overriding the defaults and
  create an override file.
  """
  overrides = parse_override_config(namespace)
  try:
    tmp_dir = tempfile.mkdtemp()
    override_config_file = os.path.join(tmp_dir, OVERRIDE_YAML)
    with open(override_config_file, 'w') as f:
      f.write(yaml.dump(overrides))

    return override_config_file
  except Exception as e:
    raise Exception("Failed to parse override config: %s" % str(e))