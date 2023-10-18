def invoke_hook_bolt_ack(self, heron_tuple, process_latency_ns):
    """invoke task hooks for every time bolt acks a tuple

    :type heron_tuple: HeronTuple
    :param heron_tuple: tuple that is acked
    :type process_latency_ns: float
    :param process_latency_ns: process latency in nano seconds
    """
    if len(self.task_hooks) > 0:
      bolt_ack_info = BoltAckInfo(heron_tuple=heron_tuple,
                                  acking_task_id=self.get_task_id(),
                                  process_latency_ms=process_latency_ns * system_constants.NS_TO_MS)
      for task_hook in self.task_hooks:
        task_hook.bolt_ack(bolt_ack_info)