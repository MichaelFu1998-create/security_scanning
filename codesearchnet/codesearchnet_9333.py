def _wait_for_any_job(provider, job_ids, poll_interval):
  """Waits until any of the listed jobs is not running.

  In particular, if any of the jobs sees one of its tasks fail,
  we count the whole job as failing (but do not terminate the remaining
  tasks ourselves).

  Args:
    provider: job service provider
    job_ids: a list of job IDs (string) to wait for
    poll_interval: integer seconds to wait between iterations

  Returns:
    A set of the jobIDs with still at least one running task.
  """
  if not job_ids:
    return
  while True:
    tasks = provider.lookup_job_tasks({'*'}, job_ids=job_ids)
    running_jobs = set()
    failed_jobs = set()
    for t in tasks:
      status = t.get_field('task-status')
      job_id = t.get_field('job-id')
      if status in ['FAILURE', 'CANCELED']:
        failed_jobs.add(job_id)
      if status == 'RUNNING':
        running_jobs.add(job_id)
    remaining_jobs = running_jobs.difference(failed_jobs)
    if failed_jobs or len(remaining_jobs) != len(job_ids):
      return remaining_jobs
    SLEEP_FUNCTION(poll_interval)