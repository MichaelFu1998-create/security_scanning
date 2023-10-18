def lookup_job_tasks(self,
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
                       page_size=0):
    """Yields operations based on the input criteria.

    If any of the filters are empty or {'*'}, then no filtering is performed on
    that field. Filtering by both a job id list and job name list is
    unsupported.

    Args:
      statuses: {'*'}, or a list of job status strings to return. Valid
        status strings are 'RUNNING', 'SUCCESS', 'FAILURE', or 'CANCELED'.
      user_ids: a list of ids for the user(s) who launched the job.
      job_ids: a list of job ids to return.
      job_names: a list of job names to return.
      task_ids: a list of specific tasks within the specified job(s) to return.
      task_attempts: a list of specific attempts within the specified tasks(s)
        to return.
      labels: a list of LabelParam with user-added labels. All labels must
              match the task being fetched.
      create_time_min: a timezone-aware datetime value for the earliest create
                       time of a task, inclusive.
      create_time_max: a timezone-aware datetime value for the most recent
                       create time of a task, inclusive.
      max_tasks: the maximum number of job tasks to return or 0 for no limit.
      page_size: the page size to use for each query to the pipelins API.

    Raises:
      ValueError: if both a job id list and a job name list are provided

    Yeilds:
      Genomics API Operations objects.
    """

    # Build a filter for operations to return
    ops_filter = self._build_query_filter(
        statuses, user_ids, job_ids, job_names, task_ids, task_attempts, labels,
        create_time_min, create_time_max)

    # Execute the operations.list() API to get batches of operations to yield
    page_token = None
    tasks_yielded = 0
    while True:
      # If max_tasks is set, let operations.list() know not to send more than
      # we need.
      max_to_fetch = None
      if max_tasks:
        max_to_fetch = max_tasks - tasks_yielded
      ops, page_token = self._operations_list(ops_filter, max_to_fetch,
                                              page_size, page_token)

      for op in ops:
        yield op
        tasks_yielded += 1

      assert (max_tasks >= tasks_yielded or not max_tasks)
      if not page_token or 0 < max_tasks <= tasks_yielded:
        break