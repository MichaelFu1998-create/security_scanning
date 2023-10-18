def _init_multi_count_metrics(self, pplan_helper):
    """Initializes the default values for a necessary set of MultiCountMetrics"""
    to_init = [self.metrics[i] for i in self.to_multi_init
               if i in self.metrics and isinstance(self.metrics[i], MultiCountMetric)]
    for out_stream in pplan_helper.get_my_spout().outputs:
      stream_id = out_stream.stream.id
      for metric in to_init:
        metric.add_key(stream_id)