def _dominant_task_for_jobs(tasks):
  """A list with, for each job, its dominant task.

  The dominant task is the one that exemplifies its job's
  status. It is either:
  - the first (FAILURE or CANCELED) task, or if none
  - the first RUNNING task, or if none
  - the first SUCCESS task.

  Args:
    tasks: a list of tasks to consider

  Returns:
    A list with, for each job, its dominant task.
  """

  per_job = _group_tasks_by_jobid(tasks)

  ret = []
  for job_id in per_job.keys():
    tasks_in_salience_order = sorted(per_job[job_id], key=_importance_of_task)
    ret.append(tasks_in_salience_order[0])
  return ret