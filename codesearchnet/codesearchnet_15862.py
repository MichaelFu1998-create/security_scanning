def _set_stats_data(self, test_id, metrics):
    """
    Get summary stats data from each metric and set it in the _Analysis object specified by test_id to make it available
    for retrieval
    :return: currently always returns CONSTANTS.OK. Maybe enhanced in future to return additional status
    """
    for metric in metrics:
      self._analyses[test_id].stats_data[metric.label] = metric.summary_stats
    return CONSTANTS.OK