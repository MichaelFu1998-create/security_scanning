def calculate_key_stats(self, metric_store):
    """
    Calculate key statistics for given data and store in the class variables calculated_stats and calculated_percentiles
    calculated_stats:
      'mean', 'std', 'median', 'min', 'max'
    calculated_percentiles:
      range(5,101,5), 99
    :param dict metric_store: The metric store used to store all the parsed jmeter log data
    :return: none
    """
    stats_to_calculate = ['mean', 'std', 'median', 'min', 'max']  # TODO: get input from user
    percentiles_to_calculate = range(5, 101, 5)  # TODO: get input from user
    percentiles_to_calculate.append(99)
    for transaction in metric_store['t'].keys():
      transaction_key = transaction + '.' + 'ResponseTime'
      # For ResponseTime and ResponseSize, each timestamp has a list of values associated with it.
      # Using heapq.merge to merge all the lists into a single list to be passed to numpy.
      self.calculated_stats[transaction_key], self.calculated_percentiles[transaction_key] = \
          naarad.utils.calculate_stats(list(heapq.merge(*metric_store['t'][transaction].values())),
                                   stats_to_calculate, percentiles_to_calculate)
      self.update_summary_stats(transaction_key)
      transaction_key = transaction + '.' + 'qps'
      if len(metric_store['qps'][transaction].values()) > 0:
        self.calculated_stats[transaction_key], self.calculated_percentiles[transaction_key] = \
            naarad.utils.calculate_stats(metric_store['qps'][transaction].values(),
                                         stats_to_calculate, percentiles_to_calculate)
        self.update_summary_stats(transaction_key)
      transaction_key = transaction + '.' + 'ResponseSize'
      self.calculated_stats[transaction_key], self.calculated_percentiles[transaction_key] = \
          naarad.utils.calculate_stats(list(heapq.merge(*metric_store['by'][transaction].values())),
                                       stats_to_calculate, percentiles_to_calculate)
      self.update_summary_stats(transaction_key)
      if 'eqps' in metric_store.keys() and transaction in metric_store['eqps'].keys():
        transaction_key = transaction + '.' + 'ErrorsPerSecond'
        self.calculated_stats[transaction_key], self.calculated_percentiles[transaction_key] = \
            naarad.utils.calculate_stats(metric_store['eqps'][transaction].values(),
                                         stats_to_calculate, percentiles_to_calculate)
        self.update_summary_stats(transaction + '.' + 'ErrorsPerSecond')
      transaction_key = transaction + '.' + 'DataThroughput'
      self.calculated_stats[transaction_key], self.calculated_percentiles[transaction_key] = \
          naarad.utils.calculate_stats(metric_store['thr'][transaction].values(),
                                       stats_to_calculate, percentiles_to_calculate)
      self.update_summary_stats(transaction_key)
    return None