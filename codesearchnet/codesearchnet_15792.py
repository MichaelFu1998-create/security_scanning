def discover_by_name(input_directory, output_directory):
  """
  Auto discover metric types from the files that exist in input_directory and return a list of metrics
  :param: input_directory: The location to scan for log files
  :param: output_directory: The location for the report
  """
  metric_list = []
  log_files = os.listdir(input_directory)
  for log_file in log_files:
    if log_file in CONSTANTS.SUPPORTED_FILENAME_MAPPING.keys():
      metric_list.append(initialize_metric(CONSTANTS.SUPPORTED_FILENAME_MAPPING[log_file], [log_file], None, [], output_directory, CONSTANTS.RESOURCE_PATH,
                                           CONSTANTS.SUPPORTED_FILENAME_MAPPING[log_file], None, None, {}, None, None, {}))
    else:
      logger.warning('Unable to determine metric type for file: %s', log_file)
  return metric_list