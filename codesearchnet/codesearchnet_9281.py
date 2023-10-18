def error_message(self):
    """Returns an error message if the operation failed for any reason.

    Failure as defined here means; ended for any reason other than 'success'.
    This means that a successful cancelation will also create an error message
    here.

    Returns:
      string, string will be empty if job did not error.
    """
    if 'error' in self._op:
      if 'task-id' in self._op['metadata']['labels']:
        job_id = self._op['metadata']['labels']['task-id']
      else:
        job_id = self._op['metadata']['labels']['job-id']
      return 'Error in job %s - code %s: %s' % (job_id,
                                                self._op['error']['code'],
                                                self._op['error']['message'])
    else:
      return ''