def to_serializable(self):
    """Return a dict populated for serialization (as YAML/JSON)."""

    task_metadata = self.task_metadata
    task_params = self.task_params
    task_resources = self.task_resources

    # The only required field is the task-id, even if it is None
    task_id = None
    if task_metadata.get('task-id') is not None:
      task_id = str(task_metadata.get('task-id'))

    task = {'task-id': task_id}
    task['create-time'] = task_metadata.get('create-time')
    task['task-attempt'] = task_metadata.get('task-attempt')

    if task_resources.logging_path:
      task['logging-path'] = str(task_resources.logging_path.uri)

    task['labels'] = {var.name: var.value for var in task_params['labels']}

    task['envs'] = {var.name: var.value for var in task_params['envs']}

    task['inputs'] = {
        var.name: var.value
        for var in task_params['inputs']
        if not var.recursive
    }
    task['input-recursives'] = {
        var.name: var.value
        for var in task_params['inputs']
        if var.recursive
    }
    task['outputs'] = {
        var.name: var.value
        for var in task_params['outputs']
        if not var.recursive
    }
    task['output-recursives'] = {
        var.name: var.value
        for var in task_params['outputs']
        if var.recursive
    }

    return _remove_empty_items(task, ['task-id'])