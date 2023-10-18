def handle_start_stateful_processing(self, start_msg):
    """Called when we receive StartInstanceStatefulProcessing message
    :param start_msg: StartInstanceStatefulProcessing type
    """
    Log.info("Received start stateful processing for %s" % start_msg.checkpoint_id)
    self.is_stateful_started = True
    self.start_instance_if_possible()