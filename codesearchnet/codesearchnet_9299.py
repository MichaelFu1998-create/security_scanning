def _get_localization_env(self, inputs, user_project):
    """Return a dict with variables for the 'localization' action."""

    # Add variables for paths that need to be localized, for example:
    # INPUT_COUNT: 1
    # INPUT_0: MY_INPUT_FILE
    # INPUT_RECURSIVE_0: 0
    # INPUT_SRC_0: gs://mybucket/mypath/myfile
    # INPUT_DST_0: /mnt/data/inputs/mybucket/mypath/myfile

    non_empty_inputs = [var for var in inputs if var.value]
    env = {'INPUT_COUNT': str(len(non_empty_inputs))}

    for idx, var in enumerate(non_empty_inputs):
      env['INPUT_{}'.format(idx)] = var.name
      env['INPUT_RECURSIVE_{}'.format(idx)] = str(int(var.recursive))
      env['INPUT_SRC_{}'.format(idx)] = var.value

      # For wildcard paths, the destination must be a directory
      dst = os.path.join(providers_util.DATA_MOUNT_POINT, var.docker_path)
      path, filename = os.path.split(dst)
      if '*' in filename:
        dst = '{}/'.format(path)
      env['INPUT_DST_{}'.format(idx)] = dst

    env['USER_PROJECT'] = user_project

    return env