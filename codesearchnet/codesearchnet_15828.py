def aggregate_values_over_time(self, metric_store, data, groupby_name, column_name, aggregate_timestamp):
    """
    Organize and store the data from the log line into the metric store by metric type, transaction, timestamp

    :param dict metric_store: The metric store used to store all the parsed log data
    :param string data: column data in the log line
    :param string groupby_name: the group that the data belongs to
    :param string column_name: the column name of the data
    :param string aggregate_timestamp: timestamp used for storing the raw data. This accounts for aggregation time period
    :return: None
    """
    # To add overall_summary one
    if self.groupby:
      metric_data = reduce(defaultdict.__getitem__, [column_name, 'Overall_summary', aggregate_timestamp], metric_store)
      metric_data.append(float(data))
    metric_data = reduce(defaultdict.__getitem__, [column_name, groupby_name, aggregate_timestamp], metric_store)
    metric_data.append(float(data))
    return None