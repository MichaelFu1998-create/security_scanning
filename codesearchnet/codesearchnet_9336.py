def run(provider,
        job_resources,
        job_params,
        task_descriptors,
        name=None,
        dry_run=False,
        command=None,
        script=None,
        user=None,
        user_project=None,
        wait=False,
        retries=0,
        poll_interval=10,
        after=None,
        skip=False,
        project=None,
        disable_warning=False,
        unique_job_id=False):
  """Actual dsub body, post-stdout-redirection."""
  if not dry_run:
    provider_base.emit_provider_message(provider)

  if not disable_warning:
    raise ValueError('Do not use this unstable API component!')

  if command and script:
    raise ValueError('Cannot supply both a command and script value.')

  if command:
    if name:
      command_name = name
    else:
      command_name = _name_for_command(command)

    # Add the shebang line to ensure the command is treated as Bash
    script = job_model.Script(command_name, '#!/usr/bin/env bash\n' + command)
  elif script:
    # Read the script file
    script_file = dsub_util.load_file(script)
    script = job_model.Script(os.path.basename(script), script_file.read())
  else:
    raise ValueError('One of --command or a script name must be supplied')

  if retries and not wait:
    raise ValueError('Requesting retries requires requesting wait')

  # The contract with providers and downstream code is that the job_params
  # and task_params contain 'labels', 'envs', 'inputs', and 'outputs'.
  job_model.ensure_job_params_are_complete(job_params)
  job_model.ensure_task_params_are_complete(task_descriptors)

  task_ids = {
      task_descriptor.task_metadata.get('task-id')
      for task_descriptor in task_descriptors
      if task_descriptor.task_metadata.get('task-id') is not None
  }

  # Job and task parameters from the user have been validated.
  # We can now compute some job and task properties, including:
  #  job_metadata such as the job-id, create-time, user-id, etc.
  #  task_resources such as the logging_path (which may include job-id, task-id)
  job_metadata = _get_job_metadata(provider, user, name, script, task_ids,
                                   user_project, unique_job_id)
  _resolve_task_resources(job_metadata, job_resources, task_descriptors)

  # Job and task properties are now all resolved. Begin execution!
  if not dry_run:
    print('Job: %s' % job_metadata['job-id'])

  # Wait for predecessor jobs (if any)
  if after:
    if dry_run:
      print('(Pretend) waiting for: %s.' % after)
    else:
      print('Waiting for predecessor jobs to complete...')
      error_messages = _wait_after(provider, after, poll_interval, True)
      if error_messages:
        for msg in error_messages:
          print_error(msg)
        raise dsub_errors.PredecessorJobFailureError(
            'One or more predecessor jobs completed but did not succeed.',
            error_messages, None)

  # Launch all the job tasks!
  job_descriptor = job_model.JobDescriptor(job_metadata, job_params,
                                           job_resources, task_descriptors)
  launched_job = provider.submit_job(job_descriptor, skip)

  if not dry_run:
    if launched_job['job-id'] == dsub_util.NO_JOB:
      print('Job output already present, skipping new job submission.')
      return {'job-id': dsub_util.NO_JOB}
    print('Launched job-id: %s' % launched_job['job-id'])
    if launched_job.get('task-id'):
      print('%s task(s)' % len(launched_job['task-id']))
    print('To check the status, run:')
    print("  dstat %s --jobs '%s' --users '%s' --status '*'" %
          (provider_base.get_dstat_provider_args(provider, project),
           launched_job['job-id'], launched_job['user-id']))
    print('To cancel the job, run:')
    print("  ddel %s --jobs '%s' --users '%s'" %
          (provider_base.get_ddel_provider_args(provider, project),
           launched_job['job-id'], launched_job['user-id']))

  # Poll for job completion
  if wait:
    print('Waiting for job to complete...')

    if retries:
      error_messages = _wait_and_retry(provider, job_metadata['job-id'],
                                       poll_interval, retries, job_descriptor)
    else:
      error_messages = _wait_after(provider, [job_metadata['job-id']],
                                   poll_interval, False)
    if error_messages:
      for msg in error_messages:
        print_error(msg)
      raise dsub_errors.JobExecutionError(
          'One or more jobs finished with status FAILURE or CANCELED'
          ' during wait.', error_messages, launched_job)

  return launched_job