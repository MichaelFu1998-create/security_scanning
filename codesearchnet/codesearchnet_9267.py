def _build_pipeline_docker_command(cls, script_name, inputs, outputs, envs):
    """Return a multi-line string of the full pipeline docker command."""

    # We upload the user script as an environment argument
    # and write it to SCRIPT_DIR (preserving its local file name).
    #
    # The docker_command:
    # * writes the script body to a file
    # * installs gcloud if there are recursive copies to do
    # * sets environment variables for inputs with wildcards
    # * sets environment variables for recursive input directories
    # * recursively copies input directories
    # * creates output directories
    # * sets environment variables for recursive output directories
    # * sets the DATA_ROOT environment variable to /mnt/data
    # * sets the working directory to ${DATA_ROOT}
    # * executes the user script
    # * recursively copies output directories
    recursive_input_dirs = [
        var for var in inputs if var.recursive and var.value
    ]
    recursive_output_dirs = [
        var for var in outputs if var.recursive and var.value
    ]

    install_cloud_sdk = ''
    if recursive_input_dirs or recursive_output_dirs:
      install_cloud_sdk = INSTALL_CLOUD_SDK

    export_input_dirs = ''
    copy_input_dirs = ''
    if recursive_input_dirs:
      export_input_dirs = providers_util.build_recursive_localize_env(
          providers_util.DATA_MOUNT_POINT, inputs)
      copy_input_dirs = providers_util.build_recursive_localize_command(
          providers_util.DATA_MOUNT_POINT, inputs, job_model.P_GCS)

    export_output_dirs = ''
    copy_output_dirs = ''
    if recursive_output_dirs:
      export_output_dirs = providers_util.build_recursive_gcs_delocalize_env(
          providers_util.DATA_MOUNT_POINT, outputs)
      copy_output_dirs = providers_util.build_recursive_delocalize_command(
          providers_util.DATA_MOUNT_POINT, outputs, job_model.P_GCS)

    docker_paths = [
        var.docker_path if var.recursive else os.path.dirname(var.docker_path)
        for var in outputs
        if var.value
    ]

    mkdirs = '\n'.join([
        'mkdir -p {0}/{1}'.format(providers_util.DATA_MOUNT_POINT, path)
        for path in docker_paths
    ])

    inputs_with_wildcards = [
        var for var in inputs if not var.recursive and var.docker_path and
        '*' in os.path.basename(var.docker_path)
    ]
    export_inputs_with_wildcards = '\n'.join([
        'export {0}="{1}/{2}"'.format(var.name, providers_util.DATA_MOUNT_POINT,
                                      var.docker_path)
        for var in inputs_with_wildcards
    ])

    export_empty_envs = '\n'.join([
        'export {0}=""'.format(var.name)
        for var in envs | inputs | outputs
        if not var.value
    ])

    return DOCKER_COMMAND.format(
        mk_runtime_dirs=MK_RUNTIME_DIRS_COMMAND,
        script_path='%s/%s' % (providers_util.SCRIPT_DIR, script_name),
        install_cloud_sdk=install_cloud_sdk,
        export_inputs_with_wildcards=export_inputs_with_wildcards,
        export_input_dirs=export_input_dirs,
        copy_input_dirs=copy_input_dirs,
        mk_output_dirs=mkdirs,
        export_output_dirs=export_output_dirs,
        export_empty_envs=export_empty_envs,
        tmpdir=providers_util.TMP_DIR,
        working_dir=providers_util.WORKING_DIR,
        copy_output_dirs=copy_output_dirs)