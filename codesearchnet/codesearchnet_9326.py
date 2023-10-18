def _resolve_task_logging(job_metadata, job_resources, task_descriptors):
  """Resolve the logging path from job and task properties.

  Args:
    job_metadata: Job metadata, such as job-id, job-name, and user-id.
    job_resources: Resources specified such as ram, cpu, and logging path.
    task_descriptors: Task metadata, parameters, and resources.

  Resolve the logging path, which may have substitution parameters such as
  job-id, task-id, user-id, and job-name.
  """
  if not job_resources.logging:
    return

  for task_descriptor in task_descriptors:
    logging_uri = provider_base.format_logging_uri(
        job_resources.logging.uri, job_metadata, task_descriptor.task_metadata)
    logging_path = job_model.LoggingParam(logging_uri,
                                          job_resources.logging.file_provider)

    if task_descriptor.task_resources:
      task_descriptor.task_resources = task_descriptor.task_resources._replace(
          logging_path=logging_path)
    else:
      task_descriptor.task_resources = job_model.Resources(
          logging_path=logging_path)