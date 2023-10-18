def _get_delocalization_env(self, outputs, user_project):
    """Return a dict with variables for the 'delocalization' action."""

    # Add variables for paths that need to be delocalized, for example:
    # OUTPUT_COUNT: 1
    # OUTPUT_0: MY_OUTPUT_FILE
    # OUTPUT_RECURSIVE_0: 0
    # OUTPUT_SRC_0: gs://mybucket/mypath/myfile
    # OUTPUT_DST_0: /mnt/data/outputs/mybucket/mypath/myfile

    non_empty_outputs = [var for var in outputs if var.value]
    env = {'OUTPUT_COUNT': str(len(non_empty_outputs))}

    for idx, var in enumerate(non_empty_outputs):
      env['OUTPUT_{}'.format(idx)] = var.name
      env['OUTPUT_RECURSIVE_{}'.format(idx)] = str(int(var.recursive))
      env['OUTPUT_SRC_{}'.format(idx)] = os.path.join(
          providers_util.DATA_MOUNT_POINT, var.docker_path)

      # For wildcard paths, the destination must be a directory
      if '*' in var.uri.basename:
        dst = var.uri.path
      else:
        dst = var.uri
      env['OUTPUT_DST_{}'.format(idx)] = dst

    env['USER_PROJECT'] = user_project

    return env