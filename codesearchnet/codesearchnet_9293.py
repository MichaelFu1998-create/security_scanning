def _delocalize_outputs_commands(self, task_dir, outputs, user_project):
    """Copy outputs from local disk to GCS."""
    commands = []
    for o in outputs:
      if o.recursive or not o.value:
        continue

      # The destination path is o.uri.path, which is the target directory
      # (rather than o.uri, which includes the filename or wildcard).
      dest_path = o.uri.path
      local_path = task_dir + '/' + _DATA_SUBDIR + '/' + o.docker_path

      if o.file_provider == job_model.P_LOCAL:
        commands.append('mkdir -p "%s"' % dest_path)

      # Use gsutil even for local files (explained in _localize_inputs_command).
      if o.file_provider in [job_model.P_LOCAL, job_model.P_GCS]:
        if user_project:
          command = 'gsutil -u %s -mq cp "%s" "%s"' % (user_project, local_path,
                                                       dest_path)
        else:
          command = 'gsutil -mq cp "%s" "%s"' % (local_path, dest_path)
        commands.append(command)

    return '\n'.join(commands)