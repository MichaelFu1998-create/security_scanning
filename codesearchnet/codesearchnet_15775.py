def extract_diff_sla_from_config_file(obj, options_file):
  """
  Helper function to parse diff config file, which contains SLA rules for diff comparisons
  """
  rule_strings = {}
  config_obj = ConfigParser.ConfigParser()
  config_obj.optionxform = str
  config_obj.read(options_file)
  for section in config_obj.sections():
    rule_strings, kwargs = get_rule_strings(config_obj, section)
    for (key, val) in rule_strings.iteritems():
      set_sla(obj, section, key, val)