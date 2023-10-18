def _task_sort_function(task):
  """Return a tuple for sorting 'most recent first'."""
  return (task.get_field('create-time'), int(task.get_field('task-id', 0)),
          int(task.get_field('task-attempt', 0)))