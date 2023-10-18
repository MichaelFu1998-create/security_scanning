def handle_restore_instance_state(self, restore_msg):
    """Called when we receive RestoreInstanceStateRequest message
    :param restore_msg: RestoreInstanceStateRequest type
    """
    Log.info("Restoring instance state to checkpoint %s" % restore_msg.state.checkpoint_id)
    # Stop the instance
    if self.is_stateful_started:
      self.my_instance.py_class.stop()
      self.my_instance.py_class.clear_collector()
      self.is_stateful_started = False

    # Clear all buffers
    self.in_stream.clear()
    self.out_stream.clear()

    # Deser the state
    if self.stateful_state is not None:
      self.stateful_state.clear()
    if restore_msg.state.state is not None and restore_msg.state.state:
      try:
        self.stateful_state = self.serializer.deserialize(restore_msg.state.state)
      except Exception as e:
        raise RuntimeError("Could not serialize state during restore " + str(e))
    else:
      Log.info("The restore request does not have an actual state")
    if self.stateful_state is None:
      self.stateful_state = HashMapState()

    Log.info("Instance restore state deserialized")

    # Send the response back
    resp = ckptmgr_pb2.RestoreInstanceStateResponse()
    resp.status.status = common_pb2.StatusCode.Value("OK")
    resp.checkpoint_id = restore_msg.state.checkpoint_id
    self._stmgr_client.send_message(resp)