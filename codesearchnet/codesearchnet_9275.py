def _build_pipeline_request(self, task_view):
    """Returns a Pipeline objects for the job."""
    job_metadata = task_view.job_metadata
    job_params = task_view.job_params
    job_resources = task_view.job_resources
    task_metadata = task_view.task_descriptors[0].task_metadata
    task_params = task_view.task_descriptors[0].task_params
    task_resources = task_view.task_descriptors[0].task_resources

    script = task_view.job_metadata['script']

    reserved_labels = google_base.build_pipeline_labels(
        job_metadata, task_metadata, task_id_pattern='task-%d')

    # Build the ephemeralPipeline for this job.
    # The ephemeralPipeline definition changes for each job because file
    # parameters localCopy.path changes based on the remote_uri.
    pipeline = _Pipelines.build_pipeline(
        project=self._project,
        zones=job_resources.zones,
        min_cores=job_resources.min_cores,
        min_ram=job_resources.min_ram,
        disk_size=job_resources.disk_size,
        boot_disk_size=job_resources.boot_disk_size,
        preemptible=job_resources.preemptible,
        accelerator_type=job_resources.accelerator_type,
        accelerator_count=job_resources.accelerator_count,
        image=job_resources.image,
        script_name=script.name,
        envs=job_params['envs'] | task_params['envs'],
        inputs=job_params['inputs'] | task_params['inputs'],
        outputs=job_params['outputs'] | task_params['outputs'],
        pipeline_name=job_metadata['pipeline-name'])

    # Build the pipelineArgs for this job.
    logging_uri = task_resources.logging_path.uri
    scopes = job_resources.scopes or google_base.DEFAULT_SCOPES
    pipeline.update(
        _Pipelines.build_pipeline_args(self._project, script.value, job_params,
                                       task_params, reserved_labels,
                                       job_resources.preemptible, logging_uri,
                                       scopes, job_resources.keep_alive))

    return pipeline