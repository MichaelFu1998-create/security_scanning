def __replace(config, wildcards, config_file):
  """For each kvp in config, do wildcard substitution on the values"""
  for config_key in config:
    config_value = config[config_key]
    original_value = config_value
    if isinstance(config_value, str):
      for token in wildcards:
        if wildcards[token]:
          config_value = config_value.replace(token, wildcards[token])
      found = re.findall(r'\${[A-Z_]+}', config_value)
      if found:
        raise ValueError("%s=%s in file %s contains unsupported or unset wildcard tokens: %s" %
                         (config_key, original_value, config_file, ", ".join(found)))
      config[config_key] = config_value
  return config