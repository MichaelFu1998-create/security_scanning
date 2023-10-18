def execute_tuple(self, stream_id, source_component, latency_in_ns):
    """Apply updates to the execute metrics"""
    self.update_count(self.EXEC_COUNT, key=stream_id)
    self.update_reduced_metric(self.EXEC_LATENCY, latency_in_ns, stream_id)
    self.update_count(self.EXEC_TIME_NS, incr_by=latency_in_ns, key=stream_id)

    global_stream_id = source_component + "/" + stream_id
    self.update_count(self.EXEC_COUNT, key=global_stream_id)
    self.update_reduced_metric(self.EXEC_LATENCY, latency_in_ns, global_stream_id)
    self.update_count(self.EXEC_TIME_NS, incr_by=latency_in_ns, key=global_stream_id)