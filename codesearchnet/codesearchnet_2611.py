def deserialize_data_tuple(self, stream_id, source_component, latency_in_ns):
    """Apply updates to the deserialization metrics"""
    self.update_count(self.TUPLE_DESERIALIZATION_TIME_NS, incr_by=latency_in_ns, key=stream_id)
    global_stream_id = source_component + "/" + stream_id
    self.update_count(self.TUPLE_DESERIALIZATION_TIME_NS, incr_by=latency_in_ns,
                      key=global_stream_id)