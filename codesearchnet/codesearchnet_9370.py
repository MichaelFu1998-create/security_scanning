def _from_yaml_v0(cls, job):
    """Populate a JobDescriptor from the local provider's original meta.yaml.

    The local job provider had the first incarnation of a YAML file for each
    task. That idea was extended here in the JobDescriptor and the local
    provider adopted the JobDescriptor.to_yaml() call to write its meta.yaml.

    The JobDescriptor.from_yaml() detects if it receives a local provider's
    "v0" meta.yaml and calls this function.

    Args:
      job: an object produced from decoding meta.yaml.

    Returns:
      A JobDescriptor populated as best we can from the old meta.yaml.
    """

    # The v0 meta.yaml only contained:
    #   create-time, job-id, job-name, logging, task-id
    #   labels, envs, inputs, outputs
    # It did NOT contain user-id.
    # dsub-version might be there as a label.

    job_metadata = {}
    for key in ['job-id', 'job-name', 'create-time']:
      job_metadata[key] = job.get(key)

    # Make sure that create-time string is turned into a datetime
    job_metadata['create-time'] = dsub_util.replace_timezone(
        datetime.datetime.strptime(job['create-time'], '%Y-%m-%d %H:%M:%S.%f'),
        tzlocal())

    # The v0 meta.yaml contained a "logging" field which was the task-specific
    # logging path. It did not include the actual "--logging" value the user
    # specified.
    job_resources = Resources()

    # The v0 meta.yaml represented a single task.
    # It did not distinguish whether params were job params or task params.
    # We will treat them as either all job params or all task params, based on
    # whether the task-id is empty or an integer value.
    #
    # We also cannot distinguish whether inputs/outputs were recursive or not.
    # Just treat them all as non-recursive.
    params = {}

    # The dsub-version may be in the meta.yaml as a label. If so remove it
    # and set it as a top-level job metadata value.
    labels = job.get('labels', {})
    if 'dsub-version' in labels:
      job_metadata['dsub-version'] = labels['dsub-version']
      del labels['dsub-version']
    params['labels'] = cls._label_params_from_dict(labels)

    params['envs'] = cls._env_params_from_dict(job.get('envs', {}))
    params['inputs'] = cls._input_file_params_from_dict(
        job.get('inputs', {}), False)
    params['outputs'] = cls._output_file_params_from_dict(
        job.get('outputs', {}), False)

    if job.get('task-id') is None:
      job_params = params
      task_metadata = {'task-id': None}
      task_params = {}
    else:
      job_params = {}
      task_metadata = {'task-id': str(job.get('task-id'))}
      task_params = params

    task_resources = Resources(logging_path=job.get('logging'))

    task_descriptors = [
        TaskDescriptor.get_complete_descriptor(task_metadata, task_params,
                                               task_resources)
    ]

    return JobDescriptor.get_complete_descriptor(
        job_metadata, job_params, job_resources, task_descriptors)