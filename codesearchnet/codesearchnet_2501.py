def parse_override_config(namespace):
  """Parse the command line for overriding the defaults"""
  overrides = dict()
  for config in namespace:
    kv = config.split("=")
    if len(kv) != 2:
      raise Exception("Invalid config property format (%s) expected key=value" % config)
    if kv[1] in ['true', 'True', 'TRUE']:
      overrides[kv[0]] = True
    elif kv[1] in ['false', 'False', 'FALSE']:
      overrides[kv[0]] = False
    else:
      overrides[kv[0]] = kv[1]
  return overrides