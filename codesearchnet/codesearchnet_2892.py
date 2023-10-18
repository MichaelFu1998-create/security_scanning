def add(self, stream_id, task_ids, grouping, source_comp_name):
    """Adds the target component

    :type stream_id: str
    :param stream_id: stream id into which tuples are emitted
    :type task_ids: list of str
    :param task_ids: list of task ids to which tuples are emitted
    :type grouping: ICustomStreamGrouping object
    :param grouping: custom grouping to use
    :type source_comp_name: str
    :param source_comp_name: source component name
    """
    if stream_id not in self.targets:
      self.targets[stream_id] = []
    self.targets[stream_id].append(Target(task_ids, grouping, source_comp_name))