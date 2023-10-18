def invoke_hook_spout_fail(self, message_id, fail_latency_ns):
    """invoke task hooks for every time spout fails a tuple

    :type message_id: str
    :param message_id: message id to which a failed tuple was anchored
    :type fail_latency_ns: float
    :param fail_latency_ns: fail latency in nano seconds
    """
    if len(self.task_hooks) > 0:
      spout_fail_info = SpoutFailInfo(message_id=message_id,
                                      spout_task_id=self.get_task_id(),
                                      fail_latency_ms=fail_latency_ns * system_constants.NS_TO_MS)
      for task_hook in self.task_hooks:
        task_hook.spout_fail(spout_fail_info)