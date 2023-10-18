def initialize_metric(section, infile_list, hostname, aggr_metrics, output_directory, resource_path, label, ts_start, ts_end, rule_strings,
                      important_sub_metrics, anomaly_detection_metrics, other_options):
  """
  Initialize appropriate metric based on type of metric.
  :param: section: config section name or auto discovered metric type
  :param: infile_list: list of input log files for the metric
  :param: hostname: hostname associated with the logs origin
  :param: output_directory: report location
  :param: resource_path: resource path for report
  :param: label: label for config section or auto discovered metric type
  :param: ts_start: start time for analysis
  :param: ts_end: end time for analysis
  :param: rule_strings: list of slas
  :param: important_sub_metrics: list of important sub metrics
  :param: anomaly_detection_metrics: list of metrics to use for anomaly detection.
  :param: other_options: kwargs
  :return: metric object
  """
  metric = None
  metric_type = section.split('-')[0]
  if metric_type in metric_classes:
    if 'SAR' in metric_type:
      metric = metric_classes['SAR'](section, infile_list, hostname, aggr_metrics, output_directory, resource_path, label, ts_start, ts_end,
                                     rule_strings, important_sub_metrics, anomaly_detection_metrics, **other_options)
    else:
      metric = metric_classes[metric_type](section, infile_list, hostname, aggr_metrics, output_directory, resource_path, label, ts_start, ts_end,
                                           rule_strings, important_sub_metrics, anomaly_detection_metrics, **other_options)
  else:
    metric = Metric(section, infile_list, hostname, aggr_metrics, output_directory, resource_path, label, ts_start, ts_end, rule_strings,
                    important_sub_metrics, anomaly_detection_metrics, **other_options)
  return metric