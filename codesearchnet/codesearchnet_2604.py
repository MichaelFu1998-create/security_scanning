def serialize_data_tuple(self, stream_id, latency_in_ns):
    """Apply update to serialization metrics"""
    self.update_count(self.TUPLE_SERIALIZATION_TIME_NS, incr_by=latency_in_ns, key=stream_id)