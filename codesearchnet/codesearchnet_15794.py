def initialize_aggregate_metric(section, aggr_hosts, aggr_metrics, metrics, outdir_default, resource_path, label, ts_start, ts_end, rule_strings,
                                important_sub_metrics, anomaly_detection_metrics, other_options):
  """
  Initialize aggregate metric
  :param: section: config section name
  :param: aggr_hosts: list of hostnames to aggregate
  :param: aggr_metrics: list of metrics to aggregate
  :param: metrics: list of metric objects associated with the current naarad analysis
  :param: outdir_default: report location
  :param: resource_path: resource path for report
  :param: label: label for config section
  :param: ts_start: start time for analysis
  :param: ts_end: end time for analysis
  :param: rule_strings: list of slas
  :param: important_sub_metrics: list of important sub metrics
  :param: other_options: kwargs
  :return: metric object
  """
  metric = None
  metric_type = section.split('-')[0]
  metric = aggregate_metric_classes[metric_type](section, aggr_hosts, aggr_metrics, metrics, outdir_default, resource_path, label, ts_start, ts_end,
                                                 rule_strings, important_sub_metrics, anomaly_detection_metrics, **other_options)
  return metric