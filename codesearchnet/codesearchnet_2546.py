def _is_continue_to_work(self):
    """Checks whether we still need to do more work

    When the topology state is RUNNING:
    1. if the out_queue is not full and ack is not enabled, we could wake up next time to
       produce more tuples and push to the out_queue
    2. if the out_queue is not full but the acking is enabled, we need to make sure that
      the number of pending tuples is smaller than max_spout_pending
    3. if there are more to read, we will wake up itself next time.
    """
    if not self._is_topology_running():
      return False

    max_spout_pending = \
      self.pplan_helper.context.get_cluster_config().get(api_constants.TOPOLOGY_MAX_SPOUT_PENDING)

    if not self.acking_enabled and self.output_helper.is_out_queue_available():
      return True
    elif self.acking_enabled and self.output_helper.is_out_queue_available() and \
        len(self.in_flight_tuples) < max_spout_pending:
      return True
    elif self.acking_enabled and not self.in_stream.is_empty():
      return True
    else:
      return False