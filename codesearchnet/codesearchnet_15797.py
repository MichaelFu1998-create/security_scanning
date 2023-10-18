def aggregate_values_over_time(self, metric_store, line_data, transaction_list, metric_list, aggregate_timestamp):
    """
    Organize and store the data from the log line into the metric store by metric type, transaction, timestamp

    :param dict metric_store: The metric store used to store all the parsed jmeter log data
    :param dict line_data: dict with the extracted k:v from the log line
    :param list transaction_list: list of transaction to be used for storing the metrics from given line
    :param list metric_list: list of metrics to extract from the log line
    :param string aggregate_timestamp: timestamp used for storing the raw data. This accounts for aggregation time period
    :return: None
    """
    for metric in metric_list:
      for transaction in transaction_list:
        metric_data = reduce(defaultdict.__getitem__, [metric, transaction, aggregate_timestamp], metric_store)
        metric_data.append(float(line_data.get(metric)))
    return None