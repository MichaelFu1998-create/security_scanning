def get_job_and_task_param(job_params, task_params, field):
  """Returns a dict combining the field for job and task params."""
  return job_params.get(field, set()) | task_params.get(field, set())