def dstat_job_producer(provider,
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
                       full_output=False,
                       summary_output=False,
                       poll_interval=0,
                       raw_format=False):
  """Generate jobs as lists of task dicts ready for formatting/output.

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
    full_output: (bool) return all dsub fields.
    summary_output: (bool) return a summary of the job list.
    poll_interval: (int) wait time between poll events, dstat will poll jobs
                   until all jobs succeed or fail. Set to zero to disable
                   polling and return after the first lookup.
    raw_format: (bool) set True to prevent dsub from normalizing the task dict,
                this defaults to False and should only be set True if a
                provider-specific view of tasks is absolutely required.
                (NB: provider interfaces change over time, no transition path
                will be provided for users depending on this flag).

  Yields:
    lists of task dictionaries - each list representing a dstat poll event.
  """
  some_job_running = True
  while some_job_running:
    # Get a batch of jobs.
    tasks = provider.lookup_job_tasks(
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
        page_size=max_tasks)

    some_job_running = False

    formatted_tasks = []
    for task in tasks:
      if 0 < max_tasks <= len(formatted_tasks):
        break

      # Format tasks as specified.
      if raw_format:
        formatted_tasks.append(task.raw_task_data())
      else:
        formatted_tasks.append(_prepare_row(task, full_output, summary_output))

      # Determine if any of the jobs are running.
      if task.get_field('task-status') == 'RUNNING':
        some_job_running = True

    # Yield the tasks and determine if the loop should continue.
    yield formatted_tasks
    if poll_interval and some_job_running:
      time.sleep(poll_interval)
    else:
      break