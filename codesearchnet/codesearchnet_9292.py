def _localize_inputs_command(self, task_dir, inputs, user_project):
    """Returns a command that will stage inputs."""
    commands = []
    for i in inputs:
      if i.recursive or not i.value:
        continue

      source_file_path = i.uri
      local_file_path = task_dir + '/' + _DATA_SUBDIR + '/' + i.docker_path
      dest_file_path = self._get_input_target_path(local_file_path)

      commands.append('mkdir -p "%s"' % os.path.dirname(local_file_path))

      if i.file_provider in [job_model.P_LOCAL, job_model.P_GCS]:
        # The semantics that we expect here are implemented consistently in
        # "gsutil cp", and are a bit different than "cp" when it comes to
        # wildcard handling, so use it for both local and GCS:
        #
        # - `cp path/* dest/` will error if "path" has subdirectories.
        # - `cp "path/*" "dest/"` will fail (it expects wildcard expansion
        #   to come from shell).
        if user_project:
          command = 'gsutil -u %s -mq cp "%s" "%s"' % (
              user_project, source_file_path, dest_file_path)
        else:
          command = 'gsutil -mq cp "%s" "%s"' % (source_file_path,
                                                 dest_file_path)
        commands.append(command)

    return '\n'.join(commands)