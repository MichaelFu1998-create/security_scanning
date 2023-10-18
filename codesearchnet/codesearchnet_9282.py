def _format_task_name(job_id, task_id, task_attempt):
  """Create a task name from a job-id, task-id, and task-attempt.

  Task names are used internally by dsub as well as by the docker task runner.
  The name is formatted as "<job-id>.<task-id>[.task-attempt]". Task names
  follow formatting conventions allowing them to be safely used as a docker
  name.

  Args:
    job_id: (str) the job ID.
    task_id: (str) the task ID.
    task_attempt: (int) the task attempt.

  Returns:
    a task name string.
  """
  docker_name = '%s.%s' % (job_id, 'task' if task_id is None else task_id)

  if task_attempt is not None:
    docker_name += '.' + str(task_attempt)

  # Docker container names must match: [a-zA-Z0-9][a-zA-Z0-9_.-]
  # So 1) prefix it with "dsub-" and 2) change all invalid characters to "-".
  return 'dsub-{}'.format(_convert_suffix_to_docker_chars(docker_name))