def _build_pipeline_input_file_param(cls, var_name, docker_path):
    """Return a dict object representing a pipeline input argument."""

    # If the filename contains a wildcard, then the target Docker path must
    # be a directory in order to ensure consistency whether the source pattern
    # contains 1 or multiple files.
    #
    # In that case, we set the docker_path to explicitly have a trailing slash
    # (for the Pipelines API "gsutil cp" handling, and then override the
    # associated var_name environment variable in the generated Docker command.

    path, filename = os.path.split(docker_path)
    if '*' in filename:
      return cls._build_pipeline_file_param(var_name, path + '/')
    else:
      return cls._build_pipeline_file_param(var_name, docker_path)