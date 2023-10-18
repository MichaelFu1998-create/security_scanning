def get_file_environment_variables(file_params):
  """Return a dictionary of environment variables for the user container."""
  env = {}
  for param in file_params:
    # We have no cases where the environment variable provided to user
    # scripts have a trailing slash, so be sure to always strip it.
    # The case that this is specifically handling is --input-recursive and
    # --output-recursive variables, which are directory values.
    env[param.name] = os.path.join(
        DATA_MOUNT_POINT, param.docker_path.rstrip('/')) if param.value else ''
  return env