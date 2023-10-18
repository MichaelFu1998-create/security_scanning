def build_pipeline(cls, project, zones, min_cores, min_ram, disk_size,
                     boot_disk_size, preemptible, accelerator_type,
                     accelerator_count, image, script_name, envs, inputs,
                     outputs, pipeline_name):
    """Builds a pipeline configuration for execution.

    Args:
      project: string name of project.
      zones: list of zone names for jobs to be run at.
      min_cores: int number of CPU cores required per job.
      min_ram: int GB of RAM required per job.
      disk_size: int GB of disk to attach under /mnt/data.
      boot_disk_size: int GB of disk for boot.
      preemptible: use a preemptible VM for the job
      accelerator_type: string GCE defined accelerator type.
      accelerator_count: int number of accelerators of the specified type to
        attach.
      image: string Docker image name in which to run.
      script_name: file name of the script to run.
      envs: list of EnvParam objects specifying environment variables to set
        within each job.
      inputs: list of FileParam objects specifying input variables to set
        within each job.
      outputs: list of FileParam objects specifying output variables to set
        within each job.
      pipeline_name: string name of pipeline.

    Returns:
      A nested dictionary with one entry under the key ephemeralPipeline
      containing the pipeline configuration.
    """
    if min_cores is None:
      min_cores = job_model.DEFAULT_MIN_CORES
    if min_ram is None:
      min_ram = job_model.DEFAULT_MIN_RAM
    if disk_size is None:
      disk_size = job_model.DEFAULT_DISK_SIZE
    if boot_disk_size is None:
      boot_disk_size = job_model.DEFAULT_BOOT_DISK_SIZE
    if preemptible is None:
      preemptible = job_model.DEFAULT_PREEMPTIBLE

    # Format the docker command
    docker_command = cls._build_pipeline_docker_command(script_name, inputs,
                                                        outputs, envs)

    # Pipelines inputParameters can be both simple name/value pairs which get
    # set as environment variables, as well as input file paths which the
    # Pipelines controller will automatically localize to the Pipeline VM.

    # In the ephemeralPipeline object, the inputParameters are only defined;
    # the values are passed in the pipelineArgs.

    # Pipelines outputParameters are only output file paths, which the
    # Pipelines controller can automatically de-localize after the docker
    # command completes.

    # The Pipelines API does not support recursive copy of file parameters,
    # so it is implemented within the dsub-generated pipeline.
    # Any inputs or outputs marked as "recursive" are completely omitted here;
    # their environment variables will be set in the docker command, and
    # recursive copy code will be generated there as well.

    # The Pipelines API does not accept empty environment variables. Set them to
    # empty in DOCKER_COMMAND instead.
    input_envs = [{
        'name': SCRIPT_VARNAME
    }] + [{
        'name': env.name
    } for env in envs if env.value]

    input_files = [
        cls._build_pipeline_input_file_param(var.name, var.docker_path)
        for var in inputs
        if not var.recursive and var.value
    ]

    # Outputs are an array of file parameters
    output_files = [
        cls._build_pipeline_file_param(var.name, var.docker_path)
        for var in outputs
        if not var.recursive and var.value
    ]

    # The ephemeralPipeline provides the template for the pipeline.
    # pyformat: disable
    return {
        'ephemeralPipeline': {
            'projectId': project,
            'name': pipeline_name,

            # Define the resources needed for this pipeline.
            'resources': {
                'minimumCpuCores': min_cores,
                'minimumRamGb': min_ram,
                'bootDiskSizeGb': boot_disk_size,
                'preemptible': preemptible,
                'zones': google_base.get_zones(zones),
                'acceleratorType': accelerator_type,
                'acceleratorCount': accelerator_count,

                # Create a data disk that is attached to the VM and destroyed
                # when the pipeline terminates.
                'disks': [{
                    'name': 'datadisk',
                    'autoDelete': True,
                    'sizeGb': disk_size,
                    'mountPoint': providers_util.DATA_MOUNT_POINT,
                }],
            },

            'inputParameters': input_envs + input_files,
            'outputParameters': output_files,

            'docker': {
                'imageName': image,
                'cmd': docker_command,
            }
        }
    }