def from_yaml(cls, yaml_string):
    """Populate and return a JobDescriptor from a YAML string."""
    try:
      job = yaml.full_load(yaml_string)
    except AttributeError:
      # For installations that cannot update their PyYAML version
      job = yaml.load(yaml_string)

    # If the YAML does not contain a top-level dsub version, then assume that
    # the string is coming from the local provider, reading an old version of
    # its meta.yaml.
    dsub_version = job.get('dsub-version')
    if not dsub_version:
      return cls._from_yaml_v0(job)

    job_metadata = {}
    for key in [
        'job-id', 'job-name', 'task-ids', 'user-id', 'dsub-version',
        'user-project', 'script-name'
    ]:
      if job.get(key) is not None:
        job_metadata[key] = job.get(key)

    # Make sure that create-time string is turned into a datetime
    job_metadata['create-time'] = dsub_util.replace_timezone(
        job.get('create-time'), pytz.utc)

    job_resources = Resources(logging=job.get('logging'))

    job_params = {}
    job_params['labels'] = cls._label_params_from_dict(job.get('labels', {}))
    job_params['envs'] = cls._env_params_from_dict(job.get('envs', {}))
    job_params['inputs'] = cls._input_file_params_from_dict(
        job.get('inputs', {}), False)
    job_params['input-recursives'] = cls._input_file_params_from_dict(
        job.get('input-recursives', {}), True)
    job_params['outputs'] = cls._output_file_params_from_dict(
        job.get('outputs', {}), False)
    job_params['output-recursives'] = cls._output_file_params_from_dict(
        job.get('output-recursives', {}), True)
    job_params['mounts'] = cls._mount_params_from_dict(job.get('mounts', {}))

    task_descriptors = []
    for task in job.get('tasks', []):
      task_metadata = {'task-id': task.get('task-id')}

      # Old instances of the meta.yaml do not have a task create time.
      create_time = task.get('create-time')
      if create_time:
        task_metadata['create-time'] = dsub_util.replace_timezone(
            create_time, pytz.utc)

      if task.get('task-attempt') is not None:
        task_metadata['task-attempt'] = task.get('task-attempt')

      task_params = {}
      task_params['labels'] = cls._label_params_from_dict(
          task.get('labels', {}))
      task_params['envs'] = cls._env_params_from_dict(task.get('envs', {}))
      task_params['inputs'] = cls._input_file_params_from_dict(
          task.get('inputs', {}), False)
      task_params['input-recursives'] = cls._input_file_params_from_dict(
          task.get('input-recursives', {}), True)
      task_params['outputs'] = cls._output_file_params_from_dict(
          task.get('outputs', {}), False)
      task_params['output-recursives'] = cls._output_file_params_from_dict(
          task.get('output-recursives', {}), True)

      task_resources = Resources(logging_path=task.get('logging-path'))

      task_descriptors.append(
          TaskDescriptor(task_metadata, task_params, task_resources))

    return JobDescriptor(job_metadata, job_params, job_resources,
                         task_descriptors)