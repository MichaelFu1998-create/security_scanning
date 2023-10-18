def get_rule_strings(config_obj, section):
  """
  Extract rule strings from a section
  :param config_obj: ConfigParser object
  :param section: Section name
  :return: the rule strings
  """
  rule_strings = {}
  kwargs = dict(config_obj.items(section))
  for key in kwargs.keys():
    if key.endswith('.sla'):
      rule_strings[key.replace('.sla', '')] = kwargs[key]
      del kwargs[key]
  return rule_strings, kwargs