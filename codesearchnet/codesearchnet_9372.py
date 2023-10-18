def find_task_descriptor(self, task_id):
    """Returns the task_descriptor corresponding to task_id."""

    # It is not guaranteed that the index will be task_id - 1 when --tasks is
    # used with a min/max range.
    for task_descriptor in self.task_descriptors:
      if task_descriptor.task_metadata.get('task-id') == task_id:
        return task_descriptor
    return None