def failed_tuple(self, stream_id, fail_latency_ns):
    """Apply updates to the fail metrics"""
    self.update_count(self.FAIL_COUNT, key=stream_id)
    self.update_reduced_metric(self.FAIL_LATENCY, fail_latency_ns, key=stream_id)