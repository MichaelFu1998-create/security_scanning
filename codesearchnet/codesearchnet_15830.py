def calc_key_stats(self, metric_store):
    """
    Calculate stats such as percentile and mean

    :param dict metric_store: The metric store used to store all the parsed log data
    :return: None
    """
    stats_to_calculate = ['mean', 'std', 'min', 'max']  # TODO: get input from user
    percentiles_to_calculate = range(0, 100, 1)  # TODO: get input from user
    for column, groups_store in metric_store.items():
      for group, time_store in groups_store.items():
        data = metric_store[column][group].values()
        if self.groupby:
          column_name = group + '.' + column
        else:
          column_name = column
        if column.startswith('qps'):
          self.calculated_stats[column_name], self.calculated_percentiles[column_name] = naarad.utils.calculate_stats(data, stats_to_calculate, percentiles_to_calculate)
        else:
          self.calculated_stats[column_name], self.calculated_percentiles[column_name] = naarad.utils.calculate_stats(list(heapq.merge(*data)), stats_to_calculate,
                                                                                                            percentiles_to_calculate)
        self.update_summary_stats(column_name)