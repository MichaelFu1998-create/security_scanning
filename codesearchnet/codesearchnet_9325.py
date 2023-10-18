def _get_job_metadata(provider, user_id, job_name, script, task_ids,
                      user_project, unique_job_id):
  """Allow provider to extract job-specific metadata from command-line args.

  Args:
    provider: job service provider
    user_id: user submitting the job
    job_name: name for the job
    script: the script to run
    task_ids: a set of the task-ids for all tasks in the job
    user_project: name of the project to be billed for the request
    unique_job_id: generate a unique job id

  Returns:
    A dictionary of job-specific metadata (such as job id, name, etc.)
  """
  create_time = dsub_util.replace_timezone(datetime.datetime.now(), tzlocal())
  user_id = user_id or dsub_util.get_os_user()
  job_metadata = provider.prepare_job_metadata(script.name, job_name, user_id,
                                               create_time)
  if unique_job_id:
    job_metadata['job-id'] = uuid.uuid4().hex

  job_metadata['create-time'] = create_time
  job_metadata['script'] = script
  job_metadata['user-project'] = user_project
  if task_ids:
    job_metadata['task-ids'] = dsub_util.compact_interval_string(list(task_ids))

  return job_metadata