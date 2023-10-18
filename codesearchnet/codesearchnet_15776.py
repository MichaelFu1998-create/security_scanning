def parse_basic_metric_options(config_obj, section):
  """
  Parse basic options from metric sections of the config
  :param config_obj: ConfigParser object
  :param section: Section name
  :return: all the parsed options
  """
  infile = {}
  aggr_hosts = None
  aggr_metrics = None
  ts_start = None
  ts_end = None
  precision = None
  hostname = "localhost"
  rule_strings = {}
  important_sub_metrics = None
  anomaly_detection_metrics = None

  try:
    if config_obj.has_option(section, 'important_sub_metrics'):
      important_sub_metrics = config_obj.get(section, 'important_sub_metrics').split()
      config_obj.remove_option(section, 'important_sub_metrics')

    if config_obj.has_option(section, 'hostname'):
      hostname = config_obj.get(section, 'hostname')
      config_obj.remove_option(section, 'hostname')

    # 'infile' is not mandatory for aggregate metrics
    if config_obj.has_option(section, 'infile'):
      infile = config_obj.get(section, 'infile').split()
      config_obj.remove_option(section, 'infile')

    label = sanitize_string_section_name(section)
    if config_obj.has_option(section, 'ts_start'):
      ts_start = get_standardized_timestamp(config_obj.get(section, 'ts_start'), None)
      config_obj.remove_option(section, 'ts_start')
    if config_obj.has_option(section, 'ts_end'):
      ts_end = get_standardized_timestamp(config_obj.get(section, 'ts_end'), None)
      config_obj.remove_option(section, 'ts_end')
    if config_obj.has_option(section, 'precision'):
      precision = config_obj.get(section, 'precision')
      config_obj.remove_option(section, 'precision')
    # support aggregate metrics, which take aggr_hosts and aggr_metrics
    if config_obj.has_option(section, 'aggr_hosts'):
      aggr_hosts = config_obj.get(section, 'aggr_hosts')
      config_obj.remove_option(section, 'aggr_hosts')
    if config_obj.has_option(section, 'aggr_metrics'):
      aggr_metrics = config_obj.get(section, 'aggr_metrics')
      config_obj.remove_option(section, 'aggr_metrics')
    if config_obj.has_option(section, 'anomaly_detection_metrics'):
      anomaly_detection_metrics = config_obj.get(section, 'anomaly_detection_metrics').split()
      config_obj.remove_option(section, 'anomaly_detection_metrics')
    rule_strings, other_options = get_rule_strings(config_obj, section)
  except ConfigParser.NoOptionError:
    logger.exception("Exiting.... some mandatory options are missing from the config file in section: " + section)
    sys.exit()

  return (hostname, infile, aggr_hosts, aggr_metrics, label, ts_start, ts_end, precision, aggr_metrics, other_options,
         rule_strings, important_sub_metrics, anomaly_detection_metrics)