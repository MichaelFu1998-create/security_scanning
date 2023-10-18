def average_values_for_plot(self, metric_store, data, averaging_factor):
    """
    Create the time series for the various metrics, averaged over the aggregation period being used for plots

    :param dict metric_store: The metric store used to store all the parsed jmeter log data
    :param dict data: Dict with all the metric data to be output to csv
    :param float averaging_factor: averaging factor to be used for calculating the average per second metrics
    :return: None
    """
    for metric, transaction_store in metric_store.items():
      for transaction, time_store in transaction_store.items():
        for time_stamp, metric_data in sorted(time_store.items()):
          if metric in ['t', 'by']:
            data[self.get_csv(transaction, metric)].append(','.join([str(time_stamp), str(sum(map(float, metric_data)) / float(len(metric_data)))]))
            if metric == 'by':
              metric_store['thr'][transaction][time_stamp] = sum(map(float, metric_data)) / float(averaging_factor * 1024 * 1024 / 8.0)
              data[self.get_csv(transaction, 'thr')].append(','.join([str(time_stamp), str(metric_store['thr'][transaction][time_stamp])]))
          elif metric in ['qps', 'eqps']:
            data[self.get_csv(transaction, metric)].append(','.join([str(time_stamp), str(metric_data / float(averaging_factor))]))
    return None