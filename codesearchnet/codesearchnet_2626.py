def add_data_tuple(self, stream_id, new_data_tuple, tuple_size_in_bytes):
    """Add a new data tuple to the currently buffered set of tuples"""
    if (self.current_data_tuple_set is None) or \
        (self.current_data_tuple_set.stream.id != stream_id) or \
        (len(self.current_data_tuple_set.tuples) >= self.data_tuple_set_capacity) or \
        (self.current_data_tuple_size_in_bytes >= self.max_data_tuple_size_in_bytes):
      self._init_new_data_tuple(stream_id)

    added_tuple = self.current_data_tuple_set.tuples.add()
    added_tuple.CopyFrom(new_data_tuple)

    self.current_data_tuple_size_in_bytes += tuple_size_in_bytes
    self.total_data_emitted_in_bytes += tuple_size_in_bytes