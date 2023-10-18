def invoke_hook_spout_ack(self, message_id, complete_latency_ns):
    """invoke task hooks for every time spout acks a tuple

    :type message_id: str
    :param message_id: message id to which an acked tuple was anchored
    :type complete_latency_ns: float
    :param complete_latency_ns: complete latency in nano seconds
    """
    if len(self.task_hooks) > 0:
      spout_ack_info = SpoutAckInfo(message_id=message_id,
                                    spout_task_id=self.get_task_id(),
                                    complete_latency_ms=complete_latency_ns *
                                    system_constants.NS_TO_MS)
      for task_hook in self.task_hooks:
        task_hook.spout_ack(spout_ack_info)