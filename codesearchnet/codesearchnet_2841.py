def get_metrics_collector(self):
    """Returns this context's metrics collector"""
    if self.metrics_collector is None or not isinstance(self.metrics_collector, MetricsCollector):
      raise RuntimeError("Metrics collector is not registered in this context")
    return self.metrics_collector