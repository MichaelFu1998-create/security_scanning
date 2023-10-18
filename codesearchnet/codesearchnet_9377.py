def build_recursive_delocalize_command(source, outputs, file_provider):
  """Return a multi-line string with a shell script to copy recursively.

  Arguments:
    source: Folder with the data.
            For example /mnt/data
    outputs: a list of OutputFileParam.
    file_provider: file provider string used to filter the output params; the
                 returned command will only apply outputs whose file provider
                 matches this file filter.

  Returns:
    a multi-line string with a shell script that copies the inputs
    recursively to GCS.
  """
  command = _LOCALIZE_COMMAND_MAP[file_provider]
  filtered_outputs = [
      var for var in outputs
      if var.recursive and var.file_provider == file_provider
  ]

  return '\n'.join([
      textwrap.dedent("""
      for ((i = 0; i < 3; i++)); do
        if {command} {data_mount}/{docker_path} {destination_uri}; then
          break
        elif ((i == 2)); then
          2>&1 echo "Recursive de-localization failed."
          exit 1
        fi
      done
      """).format(
          command=command,
          data_mount=source.rstrip('/'),
          docker_path=var.docker_path,
          destination_uri=var.uri) for var in filtered_outputs
  ])