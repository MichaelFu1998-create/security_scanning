def parse_metric_section(config_obj, section, metric_classes, metrics, aggregate_metric_classes, outdir_default, resource_path):
  """
  Parse a metric section and create a Metric object
  :param config_obj: ConfigParser object
  :param section: Section name
  :param metric_classes: List of valid metric types
  :param metrics: List of all regular metric objects (used by aggregate metric)
  :param aggregate_metric_classes: List of all valid aggregate metric types
  :param outdir_default: Default output directory
  :param resource_path: Default resource directory
  :return: An initialized Metric object
  """
  (hostname, infile, aggr_hosts, aggr_metrics, label, ts_start, ts_end, precision, aggr_metrics, other_options,
   rule_strings, important_sub_metrics, anomaly_detection_metrics) = parse_basic_metric_options(config_obj, section)

  # TODO: Make user specify metric_type in config and not infer from section
  metric_type = section.split('-')[0]
  if metric_type in aggregate_metric_classes:
    new_metric = initialize_aggregate_metric(section, aggr_hosts, aggr_metrics, metrics, outdir_default, resource_path, label, ts_start, ts_end, rule_strings,
                                             important_sub_metrics, anomaly_detection_metrics, other_options)
  else:
    new_metric = initialize_metric(section, infile, hostname, aggr_metrics, outdir_default, resource_path, label, ts_start, ts_end, rule_strings,
                                   important_sub_metrics, anomaly_detection_metrics, other_options)
  if config_obj.has_option(section, 'ignore') and config_obj.getint(section, 'ignore') == 1:
    new_metric.ignore = True
  if config_obj.has_option(section, 'calc_metrics'):
    new_metric.calc_metrics = config_obj.get(section, 'calc_metrics')
  new_metric.precision = precision
  return new_metric