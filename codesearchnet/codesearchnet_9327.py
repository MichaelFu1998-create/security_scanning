def _wait_after(provider, job_ids, poll_interval, stop_on_failure):
  """Print status info as we wait for those jobs.

  Blocks until either all of the listed jobs succeed,
  or one of them fails.

  Args:
    provider: job service provider
    job_ids: a set of job IDs (string) to wait for
    poll_interval: integer seconds to wait between iterations
    stop_on_failure: whether to stop waiting if one of the tasks fails.

  Returns:
    Empty list if there was no error,
    a list of error messages from the failed tasks otherwise.
  """

  # Each time through the loop, the job_set is re-set to the jobs remaining to
  # check. Jobs are removed from the list when they complete.
  #
  # We exit the loop when:
  # * No jobs remain are running, OR
  # * stop_on_failure is TRUE AND at least one job returned an error

  # remove NO_JOB
  job_ids_to_check = {j for j in job_ids if j != dsub_util.NO_JOB}
  error_messages = []
  while job_ids_to_check and (not error_messages or not stop_on_failure):
    print('Waiting for: %s.' % (', '.join(job_ids_to_check)))

    # Poll until any remaining jobs have completed
    jobs_left = _wait_for_any_job(provider, job_ids_to_check, poll_interval)

    # Calculate which jobs just completed
    jobs_completed = job_ids_to_check.difference(jobs_left)

    # Get all tasks for the newly completed jobs
    tasks_completed = provider.lookup_job_tasks({'*'}, job_ids=jobs_completed)

    # We don't want to overwhelm the user with output when there are many
    # tasks per job. So we get a single "dominant" task for each of the
    # completed jobs (one that is representative of the job's fate).
    dominant_job_tasks = _dominant_task_for_jobs(tasks_completed)
    if len(dominant_job_tasks) != len(jobs_completed):
      # print info about the jobs we couldn't find
      # (should only occur for "--after" where the job ID is a typo).
      jobs_found = dsub_util.tasks_to_job_ids(dominant_job_tasks)
      jobs_not_found = jobs_completed.difference(jobs_found)
      for j in jobs_not_found:
        error = '%s: not found' % j
        print_error('  %s' % error)
        error_messages += [error]

    # Print the dominant task for the completed jobs
    for t in dominant_job_tasks:
      job_id = t.get_field('job-id')
      status = t.get_field('task-status')
      print('  %s: %s' % (str(job_id), str(status)))
      if status in ['FAILURE', 'CANCELED']:
        error_messages += [provider.get_tasks_completion_messages([t])]

    job_ids_to_check = jobs_left

  return error_messages