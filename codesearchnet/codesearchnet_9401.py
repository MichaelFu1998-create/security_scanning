def build_pipeline_labels(job_metadata, task_metadata, task_id_pattern=None):
  """Build a set() of standard job and task labels.

  Args:
    job_metadata: Job metadata, such as job-id, job-name, and user-id.
    task_metadata: Task metadata, such as the task-id.
    task_id_pattern: A pattern for the task-id value, such as "task-%d"; the
      original google label values could not be strictly numeric, so "task-"
      was prepended.

  Returns:
    A set of standard dsub Label() objects to attach to a pipeline.
  """
  labels = {
      Label(name, job_metadata[name])
      for name in ['job-name', 'job-id', 'user-id', 'dsub-version']
  }

  task_id = task_metadata.get('task-id')
  if task_id is not None:  # Check for None (as 0 is conceivably valid)
    if task_id_pattern:
      task_id = task_id_pattern % task_id
    labels.add(Label('task-id', str(task_id)))

  task_attempt = task_metadata.get('task-attempt')
  if task_attempt is not None:
    labels.add(Label('task-attempt', str(task_attempt)))

  return labels