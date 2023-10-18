def next_tuple(self, latency_in_ns):
    """Apply updates to the next tuple metrics"""
    self.update_reduced_metric(self.NEXT_TUPLE_LATENCY, latency_in_ns)
    self.update_count(self.NEXT_TUPLE_COUNT)