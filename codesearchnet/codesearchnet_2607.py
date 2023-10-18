def acked_tuple(self, stream_id, complete_latency_ns):
    """Apply updates to the ack metrics"""
    self.update_count(self.ACK_COUNT, key=stream_id)
    self.update_reduced_metric(self.COMPLETE_LATENCY, complete_latency_ns, key=stream_id)