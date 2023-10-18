def process_incoming_tuples(self):
    """Should be called when tuple was buffered into in_stream

    This method is equivalent to ``addBoltTasks()`` but
    is designed for event-driven single-thread bolt.
    """
    # back-pressure
    if self.output_helper.is_out_queue_available():
      self._read_tuples_and_execute()
      self.output_helper.send_out_tuples()
    else:
      # update outqueue full count
      self.bolt_metrics.update_out_queue_full_count()