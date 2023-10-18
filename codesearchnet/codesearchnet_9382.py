def ddel_tasks(provider,
               user_ids=None,
               job_ids=None,
               task_ids=None,
               labels=None,
               create_time_min=None,
               create_time_max=None):
  """Kill jobs or job tasks.

  This function separates ddel logic from flag parsing and user output. Users
  of ddel who intend to access the data programmatically should use this.

  Args:
    provider: an instantiated dsub provider.
    user_ids: a set of user ids who "own" the job(s) to delete.
    job_ids: a set of job ids to delete.
    task_ids: a set of task ids to delete.
    labels: a set of LabelParam, each must match the job(s) to be cancelled.
    create_time_min: a timezone-aware datetime value for the earliest create
                     time of a task, inclusive.
    create_time_max: a timezone-aware datetime value for the most recent create
                     time of a task, inclusive.

  Returns:
    list of job ids which were deleted.
  """
  # Delete the requested jobs
  deleted_tasks, error_messages = provider.delete_jobs(
      user_ids, job_ids, task_ids, labels, create_time_min, create_time_max)

  # Emit any errors canceling jobs
  for msg in error_messages:
    print(msg)

  return deleted_tasks