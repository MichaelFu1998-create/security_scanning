def is_valid_metric_name(metric_name):
  """
  check the validity of metric_name in config; the metric_name will be used for creation of sub-dir, so only contains: alphabet, digits , '.', '-' and '_'
  :param str metric_name: metric_name
  :return: True if valid
  """
  reg = re.compile('^[a-zA-Z0-9\.\-\_]+$')
  if reg.match(metric_name) and not metric_name.startswith('.'):
    return True
  else:
    return False