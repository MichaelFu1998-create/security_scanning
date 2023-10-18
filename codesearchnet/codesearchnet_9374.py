def build_recursive_localize_env(destination, inputs):
  """Return a multi-line string with export statements for the variables.

  Arguments:
    destination: Folder where the data will be put.
                 For example /mnt/data
    inputs: a list of InputFileParam

  Returns:
    a multi-line string with a shell script that sets environment variables
    corresponding to the inputs.
  """
  export_input_dirs = '\n'.join([
      'export {0}={1}/{2}'.format(var.name, destination.rstrip('/'),
                                  var.docker_path.rstrip('/'))
      for var in inputs
      if var.recursive and var.docker_path
  ])
  return export_input_dirs