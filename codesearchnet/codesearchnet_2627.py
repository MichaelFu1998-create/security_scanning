def add_control_tuple(self, new_control_tuple, tuple_size_in_bytes, is_ack):
    """Add a new control (Ack/Fail) tuple to the currently buffered set of tuples

    :param is_ack: ``True`` if Ack, ``False`` if Fail
    """
    if self.current_control_tuple_set is None:
      self._init_new_control_tuple()
    elif is_ack and (len(self.current_control_tuple_set.fails) > 0 or
                     len(self.current_control_tuple_set.acks) >= self.control_tuple_set_capacity):
      self._init_new_control_tuple()
    elif not is_ack and \
        (len(self.current_control_tuple_set.acks) > 0 or
         len(self.current_control_tuple_set.fails) >= self.control_tuple_set_capacity):
      self._init_new_control_tuple()

    if is_ack:
      added_tuple = self.current_control_tuple_set.acks.add()
    else:
      added_tuple = self.current_control_tuple_set.fails.add()

    added_tuple.CopyFrom(new_control_tuple)

    self.total_data_emitted_in_bytes += tuple_size_in_bytes