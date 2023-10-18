def average_values_for_plot(self, metric_store, data, averaging_factor):
    """
    Create the time series for the various metrics, averaged over the aggregation period being used for plots

    :param dict metric_store: The metric store used to store all the parsed log data
    :param dict data: Dict with all the metric data to be output to csv
    :param float averaging_factor: averaging factor to be used for calculating the average per second metrics
    :return: None
    """
    for column, groups_store in metric_store.items():
      for group, time_store in groups_store.items():
        for time_stamp, column_data in sorted(time_store.items()):
          if column in ['qps']:
            if self.groupby:
              data[self.get_csv(column, group)].append(','.join([str(time_stamp), str(column_data / float(averaging_factor))]))
            else:
              data[self.get_csv(column)].append(','.join([str(time_stamp), str(column_data / float(averaging_factor))]))
          else:
            if self.groupby:
              data[self.get_csv(column, group)].append(','.join([str(time_stamp), str(sum(map(float, column_data)) / float(len(column_data)))]))
            else:
              data[self.get_csv(column)].append(','.join([str(time_stamp), str(sum(map(float, column_data)) / float(len(column_data)))]))
    return None