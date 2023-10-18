def aggregate_count_over_time(self, metric_store, line_data, transaction_list, aggregate_timestamp):
    """
    Organize and store the count of data from the log line into the metric store by metric type, transaction, timestamp

    :param dict metric_store: The metric store used to store all the parsed jmeter log data
    :param dict line_data: dict with the extracted k:v from the log line
    :param list transaction_list: list of transaction to be used for storing the metrics from given line
    :param string aggregate_timestamp: timestamp used for storing the raw data. This accounts for aggregation time period
    :return: None
    """
    for transaction in transaction_list:
      if line_data.get('s') == 'true':
        all_qps = metric_store['qps']
      else:
        all_qps = metric_store['eqps']
      qps = all_qps[transaction]
      if aggregate_timestamp in qps:
        qps[aggregate_timestamp] += 1
      else:
        qps[aggregate_timestamp] = 1
    return None