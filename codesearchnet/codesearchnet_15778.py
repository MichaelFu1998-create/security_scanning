def parse_global_section(config_obj, section):
  """
  Parse GLOBAL section in the config to return global settings
  :param config_obj: ConfigParser object
  :param section: Section name
  :return: ts_start and ts_end time
  """
  ts_start = None
  ts_end = None
  if config_obj.has_option(section, 'ts_start'):
    ts_start = get_standardized_timestamp(config_obj.get(section, 'ts_start'), None)
    config_obj.remove_option(section, 'ts_start')
  if config_obj.has_option(section, 'ts_end'):
    ts_end = get_standardized_timestamp(config_obj.get(section, 'ts_end'), None)
    config_obj.remove_option(section, 'ts_end')
  return ts_start, ts_end