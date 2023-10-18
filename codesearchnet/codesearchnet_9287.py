def _delocalize_logging_command(self, logging_path, user_project):
    """Returns a command to delocalize logs.

    Args:
      logging_path: location of log files.
      user_project: name of the project to be billed for the request.

    Returns:
      eg. 'gs://bucket/path/myfile' or 'gs://bucket/script-foobar-12'
    """

    # Get the logging prefix (everything up to ".log")
    logging_prefix = os.path.splitext(logging_path.uri)[0]

    # Set the provider-specific mkdir and file copy commands
    if logging_path.file_provider == job_model.P_LOCAL:
      mkdir_cmd = 'mkdir -p "%s"\n' % os.path.dirname(logging_prefix)
      cp_cmd = 'cp'
    elif logging_path.file_provider == job_model.P_GCS:
      mkdir_cmd = ''
      if user_project:
        cp_cmd = 'gsutil -u {} -mq cp'.format(user_project)
      else:
        cp_cmd = 'gsutil -mq cp'
    else:
      assert False

    # Construct the copy command
    copy_logs_cmd = textwrap.dedent("""\
      local cp_cmd="{cp_cmd}"
      local prefix="{prefix}"
    """).format(
        cp_cmd=cp_cmd, prefix=logging_prefix)

    # Build up the command
    body = textwrap.dedent("""\
      {mkdir_cmd}
      {copy_logs_cmd}
    """).format(
        mkdir_cmd=mkdir_cmd, copy_logs_cmd=copy_logs_cmd)

    return body