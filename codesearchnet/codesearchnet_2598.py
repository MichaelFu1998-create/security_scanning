def register_metrics(self, metrics_collector, interval):
    """Registers its metrics to a given metrics collector with a given interval"""
    for field, metrics in self.metrics.items():
      metrics_collector.register_metric(field, metrics, interval)