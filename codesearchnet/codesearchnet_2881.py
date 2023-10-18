def handle_initiate_stateful_checkpoint(self, ckptmsg):
    """Called when we get InitiateStatefulCheckpoint message
    :param ckptmsg: InitiateStatefulCheckpoint type
    """
    self.in_stream.offer(ckptmsg)
    if self.my_pplan_helper.is_topology_running():
      self.my_instance.py_class.process_incoming_tuples()