def send_buffered_messages(self):
    """Send messages in out_stream to the Stream Manager"""
    while not self.out_stream.is_empty() and self._stmgr_client.is_registered:
      tuple_set = self.out_stream.poll()
      if isinstance(tuple_set, tuple_pb2.HeronTupleSet):
        tuple_set.src_task_id = self.my_pplan_helper.my_task_id
        self.gateway_metrics.update_sent_packet(tuple_set.ByteSize())
      self._stmgr_client.send_message(tuple_set)