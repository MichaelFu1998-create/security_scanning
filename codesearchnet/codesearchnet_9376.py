def build_recursive_gcs_delocalize_env(source, outputs):
  """Return a multi-line string with export statements for the variables.

  Arguments:
    source: Folder with the data.
            For example /mnt/data
    outputs: a list of OutputFileParam

  Returns:
    a multi-line string with a shell script that sets environment variables
    corresponding to the outputs.
  """
  filtered_outs = [
      var for var in outputs
      if var.recursive and var.file_provider == job_model.P_GCS
  ]
  return '\n'.join([
      'export {0}={1}/{2}'.format(var.name,
                                  source.rstrip('/'),
                                  var.docker_path.rstrip('/'))
      for var in filtered_outs
  ])