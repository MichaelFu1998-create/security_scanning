def _get_task_from_task_dir(self, job_id, user_id, task_id, task_attempt):
    """Return a Task object with this task's info."""

    # We need to be very careful about how we read and interpret the contents
    # of the task directory. The directory could be changing because a new
    # task is being created. The directory could be changing because a task
    # is ending.
    #
    # If the meta.yaml does not exist, the task does not yet exist.
    # If the meta.yaml exists, it means the task is scheduled. It does not mean
    # it is yet running.
    # If the task.pid file exists, it means that the runner.sh was started.

    task_dir = self._task_directory(job_id, task_id, task_attempt)

    job_descriptor = self._read_task_metadata(task_dir)
    if not job_descriptor:
      return None

    # If we read up an old task, the user-id will not be in the job_descriptor.
    if not job_descriptor.job_metadata.get('user-id'):
      job_descriptor.job_metadata['user-id'] = user_id

    # Get the pid of the runner
    pid = -1
    try:
      with open(os.path.join(task_dir, 'task.pid'), 'r') as f:
        pid = int(f.readline().strip())
    except (IOError, OSError):
      pass

    # Get the script contents
    script = None
    script_name = job_descriptor.job_metadata.get('script-name')
    if script_name:
      script = self._read_script(task_dir, script_name)

    # Read the files written by the runner.sh.
    # For new tasks, these may not have been written yet.
    end_time = self._get_end_time_from_task_dir(task_dir)
    last_update = self._get_last_update_time_from_task_dir(task_dir)
    events = self._get_events_from_task_dir(task_dir)
    status = self._get_status_from_task_dir(task_dir)
    log_detail = self._get_log_detail_from_task_dir(task_dir)

    # If the status file is not yet written, then mark the task as pending
    if not status:
      status = 'RUNNING'
      log_detail = ['Pending']

    return LocalTask(
        task_status=status,
        events=events,
        log_detail=log_detail,
        job_descriptor=job_descriptor,
        end_time=end_time,
        last_update=last_update,
        pid=pid,
        script=script)