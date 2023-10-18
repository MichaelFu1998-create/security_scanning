def format_logging_uri(uri, job_metadata, task_metadata):
  """Inserts task metadata into the logging URI.

  The core behavior is inspired by the Google Pipelines API:
    (1) If a the uri ends in ".log", then that is the logging path.
    (2) Otherwise, the uri is treated as "directory" for logs and a filename
        needs to be automatically generated.

  For (1), if the job is a --tasks job, then the {task-id} is inserted
  before ".log".

  For (2), the file name generated is {job-id}, or for --tasks jobs, it is
  {job-id}.{task-id}.

  In both cases .{task-attempt} is inserted before .log for --retries jobs.

  In addition, full task metadata substitution is supported. The URI
  may include substitution strings such as
  "{job-id}", "{task-id}", "{job-name}", "{user-id}", and "{task-attempt}".

  Args:
    uri: User-specified logging URI which may contain substitution fields.
    job_metadata: job-global metadata.
    task_metadata: tasks-specific metadata.

  Returns:
    The logging_uri formatted as described above.
  """

  # If the user specifies any formatting (with curly braces), then use that
  # as the format string unchanged.
  fmt = str(uri)
  if '{' not in fmt:
    if uri.endswith('.log'):
      # URI includes a filename. Trim the extension and just use the prefix.
      fmt = os.path.splitext(uri)[0]
    else:
      # URI is a path to a directory. The job-id becomes the filename prefix.
      fmt = os.path.join(uri, '{job-id}')

    # If this is a task job, add the task-id.
    if task_metadata.get('task-id') is not None:
      fmt += '.{task-id}'

    # If this is a retryable task, add the task-attempt.
    if task_metadata.get('task-attempt') is not None:
      fmt += '.{task-attempt}'

    fmt += '.log'

  return _format_task_uri(fmt, job_metadata, task_metadata)