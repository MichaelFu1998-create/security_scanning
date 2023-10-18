def _wait_and_retry(provider, job_id, poll_interval, retries, job_descriptor):
  """Wait for job and retry any tasks that fail.

  Stops retrying an individual task when: it succeeds, is canceled, or has been
  retried "retries" times.

  This function exits when there are no tasks running and there are no tasks
  eligible to be retried.

  Args:
    provider: job service provider
    job_id: a single job ID (string) to wait for
    poll_interval: integer seconds to wait between iterations
    retries: number of retries
    job_descriptor: job descriptor used to originally submit job

  Returns:
    Empty list if there was no error,
    a list containing an error message from a failed task otherwise.
  """

  while True:
    tasks = provider.lookup_job_tasks({'*'}, job_ids=[job_id])

    running_tasks = set()
    completed_tasks = set()
    canceled_tasks = set()
    fully_failed_tasks = set()
    task_fail_count = dict()

    # This is an arbitrary task that is either fully failed or canceled (with
    # preference for the former).
    message_task = None

    task_dict = dict()
    for t in tasks:
      task_id = job_model.numeric_task_id(t.get_field('task-id'))
      task_dict[task_id] = t

      status = t.get_field('task-status')
      if status == 'FAILURE':
        # Could compute this from task-attempt as well.
        task_fail_count[task_id] = task_fail_count.get(task_id, 0) + 1
        if task_fail_count[task_id] > retries:
          fully_failed_tasks.add(task_id)
          message_task = t
      elif status == 'CANCELED':
        canceled_tasks.add(task_id)
        if not message_task:
          message_task = t
      elif status == 'SUCCESS':
        completed_tasks.add(task_id)
      elif status == 'RUNNING':
        running_tasks.add(task_id)

    retry_tasks = (
        set(task_fail_count).difference(fully_failed_tasks)
        .difference(running_tasks).difference(completed_tasks)
        .difference(canceled_tasks))

    # job completed.
    if not retry_tasks and not running_tasks:
      # If there are any fully failed tasks, return the completion message of an
      # arbitrary one.
      # If not, but there are canceled tasks, return the completion message of
      # an arbitrary one.
      if message_task:
        return [provider.get_tasks_completion_messages([message_task])]

      # Otherwise successful completion.
      return []

    for task_id in retry_tasks:
      identifier = '{}.{}'.format(job_id, task_id) if task_id else job_id
      print('  {} (attempt {}) failed. Retrying.'.format(
          identifier, task_fail_count[task_id]))
      msg = task_dict[task_id].get_field('status-message')
      print('  Failure message: {}'.format(msg))

      _retry_task(provider, job_descriptor, task_id,
                  task_fail_count[task_id] + 1)

    SLEEP_FUNCTION(poll_interval)