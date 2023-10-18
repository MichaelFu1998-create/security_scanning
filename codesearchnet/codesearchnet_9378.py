def build_mount_env(source, mounts):
  """Return a multi-line string with export statements for the variables.

  Arguments:
    source: Folder with the data. For example /mnt/data
    mounts: a list of MountParam

  Returns:
    a multi-line string with a shell script that sets environment variables
    corresponding to the mounts.
  """
  return '\n'.join([
      'export {0}={1}/{2}'.format(var.name, source.rstrip('/'),
                                  var.docker_path.rstrip('/')) for var in mounts
  ])