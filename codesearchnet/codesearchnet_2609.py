def _init_multi_count_metrics(self, pplan_helper):
    """Initializes the default values for a necessary set of MultiCountMetrics"""
    # inputs
    to_in_init = [self.metrics[i] for i in self.inputs_init
                  if i in self.metrics and isinstance(self.metrics[i], MultiCountMetric)]
    for in_stream in pplan_helper.get_my_bolt().inputs:
      stream_id = in_stream.stream.id
      global_stream_id = in_stream.stream.component_name + "/" + stream_id
      for metric in to_in_init:
        metric.add_key(stream_id)
        metric.add_key(global_stream_id)
    # outputs
    to_out_init = [self.metrics[i] for i in self.outputs_init
                   if i in self.metrics and isinstance(self.metrics[i], MultiCountMetric)]
    for out_stream in pplan_helper.get_my_bolt().outputs:
      stream_id = out_stream.stream.id
      for metric in to_out_init:
        metric.add_key(stream_id)