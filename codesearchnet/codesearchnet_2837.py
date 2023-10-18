def register_metric(self, name, metric, time_bucket_in_sec):
    """Registers a new metric to this context"""
    collector = self.get_metrics_collector()
    collector.register_metric(name, metric, time_bucket_in_sec)