def numeric_task_id(task_id):
  """Converts a task-id to the numeric task-id.

  Args:
    task_id: task-id in either task-n or n format

  Returns:
    n
  """

  # This function exists to support the legacy "task-id" format in the "google"
  # provider. Google labels originally could not be numeric. When the google
  # provider is completely replaced by the google-v2 provider, this function can
  # go away.

  if task_id is not None:
    if task_id.startswith('task-'):
      return int(task_id[len('task-'):])
    else:
      return int(task_id)