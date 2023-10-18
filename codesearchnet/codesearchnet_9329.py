def _retry_task(provider, job_descriptor, task_id, task_attempt):
  """Retry task_id (numeric id) assigning it task_attempt."""
  td_orig = job_descriptor.find_task_descriptor(task_id)

  new_task_descriptors = [
      job_model.TaskDescriptor({
          'task-id': task_id,
          'task-attempt': task_attempt
      }, td_orig.task_params, td_orig.task_resources)
  ]

  # Update the logging path.
  _resolve_task_resources(job_descriptor.job_metadata,
                          job_descriptor.job_resources, new_task_descriptors)

  provider.submit_job(
      job_model.JobDescriptor(
          job_descriptor.job_metadata, job_descriptor.job_params,
          job_descriptor.job_resources, new_task_descriptors), False)