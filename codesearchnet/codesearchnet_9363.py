def ensure_task_params_are_complete(task_descriptors):
  """For each task, ensure that each task param entry is not None."""
  for task_desc in task_descriptors:
    for param in [
        'labels', 'envs', 'inputs', 'outputs', 'input-recursives',
        'output-recursives'
    ]:
      if not task_desc.task_params.get(param):
        task_desc.task_params[param] = set()