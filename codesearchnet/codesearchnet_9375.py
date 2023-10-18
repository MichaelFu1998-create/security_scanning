def build_recursive_localize_command(destination, inputs, file_provider):
  """Return a multi-line string with a shell script to copy recursively.

  Arguments:
    destination: Folder where to put the data.
                 For example /mnt/data
    inputs: a list of InputFileParam
    file_provider: file provider string used to filter the output params; the
                 returned command will only apply outputs whose file provider
                 matches this file filter.

  Returns:
    a multi-line string with a shell script that copies the inputs
    recursively from GCS.
  """
  command = _LOCALIZE_COMMAND_MAP[file_provider]
  filtered_inputs = [
      var for var in inputs
      if var.recursive and var.file_provider == file_provider
  ]

  copy_input_dirs = '\n'.join([
      textwrap.dedent("""
      mkdir -p {data_mount}/{docker_path}
      for ((i = 0; i < 3; i++)); do
        if {command} {source_uri} {data_mount}/{docker_path}; then
          break
        elif ((i == 2)); then
          2>&1 echo "Recursive localization failed."
          exit 1
        fi
      done
      chmod -R o+r {data_mount}/{docker_path}
      """).format(
          command=command,
          source_uri=var.uri,
          data_mount=destination.rstrip('/'),
          docker_path=var.docker_path) for var in filtered_inputs
  ])
  return copy_input_dirs