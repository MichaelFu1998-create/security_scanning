def calculate_stats(self):
    """
    Calculate stats with different function depending on the metric type:
    Data is recorded in memory for base metric type, and use calculate_base_metric_stats()
    Data is recorded in CSV file for other metric types, and use calculate_other_metric_stats()

    """
    metric_type = self.metric_type.split('-')[0]
    if metric_type in naarad.naarad_imports.metric_classes or metric_type in naarad.naarad_imports.aggregate_metric_classes:
      self.calculate_other_metric_stats()
    else:
      self.calculate_base_metric_stats()