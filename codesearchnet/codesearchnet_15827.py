def aggregate_count_over_time(self, metric_store, groupby_name, aggregate_timestamp):
    """
    Organize and store the count of data from the log line into the metric store by columnm, group name, timestamp

    :param dict metric_store: The metric store used to store all the parsed the log data
    :param string groupby_name: the group name that the log line belongs to
    :param string aggregate_timestamp: timestamp used for storing the raw data. This accounts for aggregation time period
    :return: None
    """
    all_qps = metric_store['qps']
    qps = all_qps[groupby_name]
    if aggregate_timestamp in qps:
      qps[aggregate_timestamp] += 1
    else:
      qps[aggregate_timestamp] = 1
    return None