def _task_directory(self, job_id, task_id, task_attempt):
    """The local dir for staging files for that particular task."""
    dir_name = 'task' if task_id is None else str(task_id)
    if task_attempt:
      dir_name = '%s.%s' % (dir_name, task_attempt)
    return self._provider_root() + '/' + job_id + '/' + dir_name