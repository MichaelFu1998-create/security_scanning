def parse_xml_jtl(self, granularity):
    """
    Parse Jmeter workload output in XML format and extract overall and per transaction data and key statistics

    :param string granularity: The time period over which to aggregate and average the raw data. Valid values are 'hour', 'minute' or 'second'
    :return: status of the metric parse
    """
    data = defaultdict(list)
    processed_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for input_file in self.infile_list:
      logger.info('Processing : %s', input_file)
      timestamp_format = None
      tree = ElementTree.parse(input_file)
      samples = tree.findall('./httpSample') + tree.findall('./sample')
      for sample in samples:
        if not timestamp_format or timestamp_format == 'unknown':
          timestamp_format = naarad.utils.detect_timestamp_format(sample.get('ts'))
        if timestamp_format == 'unknown':
          continue
        ts = naarad.utils.get_standardized_timestamp(sample.get('ts'), timestamp_format)
        if ts == -1:
          continue
        ts = naarad.utils.reconcile_timezones(ts, self.timezone, self.graph_timezone)
        aggregate_timestamp, averaging_factor = self.get_aggregation_timestamp(ts, granularity)
        self.aggregate_count_over_time(processed_data, sample, [self._sanitize_label(sample.get('lb')), 'Overall_Summary'], aggregate_timestamp)
        self.aggregate_values_over_time(processed_data, sample, [self._sanitize_label(sample.get('lb')), 'Overall_Summary'], ['t', 'by'], aggregate_timestamp)
        logger.info('Finished parsing : %s', input_file)
    logger.info('Processing metrics for output to csv')
    self.average_values_for_plot(processed_data, data, averaging_factor)
    logger.info('Writing time series csv')
    for csv in data.keys():
      self.csv_files.append(csv)
      with open(csv, 'w') as csvf:
        csvf.write('\n'.join(sorted(data[csv])))
    logger.info('Processing raw data for stats')
    self.calculate_key_stats(processed_data)
    return True