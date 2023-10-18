def task_view_generator(job_descriptor):
  """Generator that yields a task-specific view of the job.

  This generator exists to make it easy for callers to iterate over the tasks
  in a JobDescriptor. Each pass yields a new JobDescriptor with a single task.

  Args:
    job_descriptor: A JobDescriptor with 1 or more tasks.

  Yields:
    A JobDescriptor with a single task.
  """
  for task_descriptor in job_descriptor.task_descriptors:
    jd = JobDescriptor(job_descriptor.job_metadata, job_descriptor.job_params,
                       job_descriptor.job_resources, [task_descriptor])
    yield jd