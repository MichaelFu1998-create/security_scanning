def _validate_job_and_task_arguments(job_params, task_descriptors):
  """Validates that job and task argument names do not overlap."""

  if not task_descriptors:
    return

  task_params = task_descriptors[0].task_params

  # The use case for specifying a label or env/input/output parameter on
  # the command-line and also including it in the --tasks file is not obvious.
  # Should the command-line override the --tasks file? Why?
  # Until this use is articulated, generate an error on overlapping names.

  # Check labels
  from_jobs = {label.name for label in job_params['labels']}
  from_tasks = {label.name for label in task_params['labels']}

  intersect = from_jobs & from_tasks
  if intersect:
    raise ValueError(
        'Names for labels on the command-line and in the --tasks file must not '
        'be repeated: {}'.format(','.join(intersect)))

  # Check envs, inputs, and outputs, all of which must not overlap each other
  from_jobs = {
      item.name
      for item in job_params['envs'] | job_params['inputs']
      | job_params['outputs']
  }
  from_tasks = {
      item.name
      for item in task_params['envs'] | task_params['inputs']
      | task_params['outputs']
  }

  intersect = from_jobs & from_tasks
  if intersect:
    raise ValueError(
        'Names for envs, inputs, and outputs on the command-line and in the '
        '--tasks file must not be repeated: {}'.format(','.join(intersect)))