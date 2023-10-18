def get_operation_full_job_id(op):
  """Returns the job-id or job-id.task-id for the operation."""
  job_id = op.get_field('job-id')
  task_id = op.get_field('task-id')
  if task_id:
    return '%s.%s' % (job_id, task_id)
  else:
    return job_id