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

    # Server-side, we can filter on status, job_id, user_id, task_id, but there
    # is no OR filter (only AND), so we can't handle lists server side.
    # Therefore we construct a set of queries for each possible combination of
    # these criteria.
    statuses = statuses if statuses else {'*'}
    user_ids = user_ids if user_ids else {'*'}
    job_ids = job_ids if job_ids else {'*'}
    job_names = job_names if job_names else {'*'}
    task_ids = task_ids if task_ids else {'*'}
    task_attempts = task_attempts if task_attempts else {'*'}

    # The task-id label value of "task-n" instead of just "n" is a hold-over
    # from early label value character restrictions.
    # Accept both forms, "task-n" and "n", for lookups by task-id.
    task_ids = {'task-{}'.format(t) if t.isdigit() else t for t in task_ids}

    if job_ids != {'*'} and job_names != {'*'}:
      raise ValueError(
          'Filtering by both job IDs and job names is not supported')

    # AND filter rule arguments.
    labels = labels if labels else set()

    # The results of all these queries need to be sorted by create-time
    # (descending). To accomplish this, each query stream (already sorted by
    # create-time) is added to a SortedGeneratorIterator which is a wrapper
    # around a PriorityQueue of iterators (sorted by each stream's newest task's
    # create-time). A sorted list can then be built by stepping through this
    # iterator and adding tasks until none are left or we hit max_tasks.

    now = datetime.now()

    def _desc_date_sort_key(t):
      return now - dsub_util.replace_timezone(t.get_field('create-time'), None)

    query_queue = sorting_util.SortedGeneratorIterator(key=_desc_date_sort_key)
    for status, job_id, job_name, user_id, task_id, task_attempt in (
        itertools.product(statuses, job_ids, job_names, user_ids, task_ids,
                          task_attempts)):
      ops_filter = _Operations.get_filter(
          self._project,
          status=status,
          user_id=user_id,
          job_id=job_id,
          job_name=job_name,
          labels=labels,
          task_id=task_id,
          task_attempt=task_attempt,
          create_time_min=create_time_min,
          create_time_max=create_time_max)

      # The pipelines API returns operations sorted by create-time date. We can
      # use this sorting guarantee to merge-sort the streams together and only
      # retrieve more tasks as needed.
      stream = _Operations.list(self._service, ops_filter, page_size=page_size)
      query_queue.add_generator(stream)

    tasks_yielded = 0
    for task in query_queue:
      yield task
      tasks_yielded += 1
      if 0 < max_tasks <= tasks_yielded:
        break