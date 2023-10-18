def _importance_of_task(task):
  """Tuple (importance, end-time). Smaller values are more important."""
  # The status of a job is going to be determined by the roll-up of its tasks.
  # A FAILURE or CANCELED task means the job has FAILED.
  # If none, then any RUNNING task, the job is still RUNNING.
  # If none, then the job status is SUCCESS.
  #
  # Thus the dominant task for each job is one that exemplifies its
  # status:
  #
  # 1- The first (FAILURE or CANCELED) task, or if none
  # 2- The first RUNNING task, or if none
  # 3- The first SUCCESS task.
  importance = {'FAILURE': 0, 'CANCELED': 0, 'RUNNING': 1, 'SUCCESS': 2}
  return (importance[task.get_field('task-status')], task.get_field(
      'end-time', datetime.datetime.max))