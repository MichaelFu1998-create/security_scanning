def error_message(self):
    """Returns an error message if the operation failed for any reason.

    Failure as defined here means ended for any reason other than 'success'.
    This means that a successful cancelation will also return an error message.

    Returns:
      string, string will be empty if job did not error.
    """
    error = google_v2_operations.get_error(self._op)
    if error:
      job_id = self.get_field('job-id')
      task_id = self.get_field('task-id')
      task_str = job_id if task_id is None else '{} (task: {})'.format(
          job_id, task_id)

      return 'Error in {} - code {}: {}'.format(task_str, error['code'],
                                                error['message'])

    return ''