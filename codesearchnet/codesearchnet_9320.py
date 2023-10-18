def _format_task_uri(fmt, job_metadata, task_metadata):
  """Returns a URI with placeholders replaced by metadata values."""

  values = {
      'job-id': None,
      'task-id': 'task',
      'job-name': None,
      'user-id': None,
      'task-attempt': None
  }
  for key in values:
    values[key] = task_metadata.get(key) or job_metadata.get(key) or values[key]

  return fmt.format(**values)