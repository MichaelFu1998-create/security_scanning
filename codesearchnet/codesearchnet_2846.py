def invoke_hook_bolt_execute(self, heron_tuple, execute_latency_ns):
    """invoke task hooks for every time bolt processes a tuple

    :type heron_tuple: HeronTuple
    :param heron_tuple: tuple that is executed
    :type execute_latency_ns: float
    :param execute_latency_ns: execute latency in nano seconds
    """
    if len(self.task_hooks) > 0:
      bolt_execute_info = \
        BoltExecuteInfo(heron_tuple=heron_tuple,
                        executing_task_id=self.get_task_id(),
                        execute_latency_ms=execute_latency_ns * system_constants.NS_TO_MS)
      for task_hook in self.task_hooks:
        task_hook.bolt_execute(bolt_execute_info)