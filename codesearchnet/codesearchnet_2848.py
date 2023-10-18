def invoke_hook_bolt_fail(self, heron_tuple, fail_latency_ns):
    """invoke task hooks for every time bolt fails a tuple

    :type heron_tuple: HeronTuple
    :param heron_tuple: tuple that is failed
    :type fail_latency_ns: float
    :param fail_latency_ns: fail latency in nano seconds
    """
    if len(self.task_hooks) > 0:
      bolt_fail_info = BoltFailInfo(heron_tuple=heron_tuple,
                                    failing_task_id=self.get_task_id(),
                                    fail_latency_ms=fail_latency_ns * system_constants.NS_TO_MS)
      for task_hook in self.task_hooks:
        task_hook.bolt_fail(bolt_fail_info)