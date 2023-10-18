def invoke_hook_emit(self, values, stream_id, out_tasks):
    """invoke task hooks for every time a tuple is emitted in spout/bolt

    :type values: list
    :param values: values emitted
    :type stream_id: str
    :param stream_id: stream id into which tuple is emitted
    :type out_tasks: list
    :param out_tasks: list of custom grouping target task id
    """
    if len(self.task_hooks) > 0:
      emit_info = EmitInfo(values=values, stream_id=stream_id,
                           task_id=self.get_task_id(), out_tasks=out_tasks)
      for task_hook in self.task_hooks:
        task_hook.emit(emit_info)