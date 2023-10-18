def lookup_job_tasks(provider,
                     statuses,
                     user_ids=None,
                     job_ids=None,
                     job_names=None,
                     task_ids=None,
                     task_attempts=None,
                     labels=None,
                     create_time_min=None,
                     create_time_max=None,
                     max_tasks=0,
                     page_size=0,
                     summary_output=False):
  """Generate formatted jobs individually, in order of create-time.

  Args:
    provider: an instantiated dsub provider.
    statuses: a set of status strings that eligible jobs may match.
    user_ids: a set of user strings that eligible jobs may match.
    job_ids: a set of job-id strings eligible jobs may match.
    job_names: a set of job-name strings eligible jobs may match.
    task_ids: a set of task-id strings eligible tasks may match.
    task_attempts: a set of task-attempt strings eligible tasks may match.
    labels: set of LabelParam that all tasks must match.
    create_time_min: a timezone-aware datetime value for the earliest create
                     time of a task, inclusive.
    create_time_max: a timezone-aware datetime value for the most recent create
                     time of a task, inclusive.
    max_tasks: (int) maximum number of tasks to return per dstat job lookup.
    page_size: the page size to use for each query to the backend. May be
               ignored by some provider implementations.
    summary_output: (bool) summarize the job list.

  Yields:
    Individual task dictionaries with associated metadata
  """
  tasks_generator = provider.lookup_job_tasks(
      statuses,
      user_ids=user_ids,
      job_ids=job_ids,
      job_names=job_names,
      task_ids=task_ids,
      task_attempts=task_attempts,
      labels=labels,
      create_time_min=create_time_min,
      create_time_max=create_time_max,
      max_tasks=max_tasks,
      page_size=page_size)

  # Yield formatted tasks.
  for task in tasks_generator:
    yield _prepare_row(task, True, summary_output)