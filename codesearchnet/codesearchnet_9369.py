def to_serializable(self):
    """Return a dict populated for serialization (as YAML/JSON)."""

    job_metadata = self.job_metadata
    job_resources = self.job_resources
    job_params = self.job_params
    task_descriptors = self.task_descriptors

    job = {
        'job-id': job_metadata.get('job-id'),
        'job-name': job_metadata.get('job-name'),
        'user-id': job_metadata.get('user-id'),
        'create-time': job_metadata.get('create-time'),
        'dsub-version': job_metadata.get('dsub-version'),
        'user-project': job_metadata.get('user-project'),
        'task-ids': job_metadata.get('task-ids'),
        'script-name': job_metadata['script'].name,
    }

    # logging is specified as a command-line argument and is typically
    # transformed (substituting job-id). The transformed value is saved
    # on a per-task basis as the 'logging-path'.
    if job_resources.logging:
      job['logging'] = str(job_resources.logging.uri)

    job['labels'] = {var.name: var.value for var in job_params['labels']}

    job['envs'] = {var.name: var.value for var in job_params['envs']}

    job['inputs'] = {
        var.name: var.value
        for var in job_params['inputs']
        if not var.recursive
    }
    job['input-recursives'] = {
        var.name: var.value
        for var in job_params['inputs']
        if var.recursive
    }

    job['outputs'] = {
        var.name: var.value
        for var in job_params['outputs']
        if not var.recursive
    }
    job['output-recursives'] = {
        var.name: var.value
        for var in job_params['outputs']
        if var.recursive
    }
    job['mounts'] = {var.name: var.value for var in job_params['mounts']}

    tasks = []
    for task_descriptor in task_descriptors:
      tasks.append(task_descriptor.to_serializable())

    job['tasks'] = tasks

    return _remove_empty_items(job, [])