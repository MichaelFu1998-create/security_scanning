def validate_submit_args_or_fail(job_descriptor, provider_name, input_providers,
                                 output_providers, logging_providers):
  """Validate that arguments passed to submit_job have valid file providers.

  This utility function takes resources and task data args from `submit_job`
  in the base provider. This function will fail with a value error if any of the
  parameters are not valid. See the following example;

  >>> job_resources = type('', (object,),
  ...    {"logging": job_model.LoggingParam('gs://logtemp', job_model.P_GCS)})()
  >>> job_params={'inputs': set(), 'outputs': set(), 'mounts': set()}
  >>> task_descriptors = [
  ...     job_model.TaskDescriptor(None, {
  ...       'inputs': {
  ...           job_model.FileParam('IN', uri='gs://in/*',
  ...                               file_provider=job_model.P_GCS)},
  ...       'outputs': set()}, None),
  ...     job_model.TaskDescriptor(None, {
  ...       'inputs': set(),
  ...       'outputs': {
  ...           job_model.FileParam('OUT', uri='gs://out/*',
  ...                               file_provider=job_model.P_GCS)}}, None)]
  ...
  >>> validate_submit_args_or_fail(job_model.JobDescriptor(None, job_params,
  ...                              job_resources, task_descriptors),
  ...                              provider_name='MYPROVIDER',
  ...                              input_providers=[job_model.P_GCS],
  ...                              output_providers=[job_model.P_GCS],
  ...                              logging_providers=[job_model.P_GCS])
  ...
  >>> validate_submit_args_or_fail(job_model.JobDescriptor(None, job_params,
  ...                              job_resources, task_descriptors),
  ...                              provider_name='MYPROVIDER',
  ...                              input_providers=[job_model.P_GCS],
  ...                              output_providers=[job_model.P_LOCAL],
  ...                              logging_providers=[job_model.P_GCS])
  Traceback (most recent call last):
       ...
  ValueError: Unsupported output path (gs://out/*) for provider 'MYPROVIDER'.

  Args:
    job_descriptor: instance of job_model.JobDescriptor.
    provider_name: (str) the name of the execution provider.
    input_providers: (string collection) whitelist of file providers for input.
    output_providers: (string collection) whitelist of providers for output.
    logging_providers: (string collection) whitelist of providers for logging.

  Raises:
    ValueError: if any file providers do not match the whitelists.
  """
  job_resources = job_descriptor.job_resources
  job_params = job_descriptor.job_params
  task_descriptors = job_descriptor.task_descriptors

  # Validate logging file provider.
  _validate_providers([job_resources.logging], 'logging', logging_providers,
                      provider_name)

  # Validate job input and output file providers
  _validate_providers(job_params['inputs'], 'input', input_providers,
                      provider_name)
  _validate_providers(job_params['outputs'], 'output', output_providers,
                      provider_name)

  # Validate input and output file providers.
  for task_descriptor in task_descriptors:
    _validate_providers(task_descriptor.task_params['inputs'], 'input',
                        input_providers, provider_name)
    _validate_providers(task_descriptor.task_params['outputs'], 'output',
                        output_providers, provider_name)