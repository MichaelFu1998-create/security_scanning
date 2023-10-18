def acked_tuple(self, stream_id, source_component, latency_in_ns):
    """Apply updates to the ack metrics"""
    self.update_count(self.ACK_COUNT, key=stream_id)
    self.update_reduced_metric(self.PROCESS_LATENCY, latency_in_ns, stream_id)
    global_stream_id = source_component + '/' + stream_id
    self.update_count(self.ACK_COUNT, key=global_stream_id)
    self.update_reduced_metric(self.PROCESS_LATENCY, latency_in_ns, global_stream_id)