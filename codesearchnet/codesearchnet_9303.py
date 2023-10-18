def _build_pipeline_request(self, task_view):
    """Returns a Pipeline objects for the task."""
    job_metadata = task_view.job_metadata
    job_params = task_view.job_params
    job_resources = task_view.job_resources
    task_metadata = task_view.task_descriptors[0].task_metadata
    task_params = task_view.task_descriptors[0].task_params
    task_resources = task_view.task_descriptors[0].task_resources

    # Set up VM-specific variables
    mnt_datadisk = google_v2_pipelines.build_mount(
        disk=_DATA_DISK_NAME,
        path=providers_util.DATA_MOUNT_POINT,
        read_only=False)
    scopes = job_resources.scopes or google_base.DEFAULT_SCOPES

    # Set up the task labels
    labels = {
        label.name: label.value if label.value else '' for label in
        google_base.build_pipeline_labels(job_metadata, task_metadata)
        | job_params['labels'] | task_params['labels']
    }

    # Set local variables for the core pipeline values
    script = task_view.job_metadata['script']
    user_project = task_view.job_metadata['user-project'] or ''

    envs = job_params['envs'] | task_params['envs']
    inputs = job_params['inputs'] | task_params['inputs']
    outputs = job_params['outputs'] | task_params['outputs']
    mounts = job_params['mounts']
    gcs_mounts = param_util.get_gcs_mounts(mounts)

    persistent_disk_mount_params = param_util.get_persistent_disk_mounts(mounts)

    persistent_disks = [
        google_v2_pipelines.build_disk(
            name=disk.name.replace('_', '-'),  # Underscores not allowed
            size_gb=disk.disk_size or job_model.DEFAULT_MOUNTED_DISK_SIZE,
            source_image=disk.value,
            disk_type=disk.disk_type or job_model.DEFAULT_DISK_TYPE)
        for disk in persistent_disk_mount_params
    ]
    persistent_disk_mounts = [
        google_v2_pipelines.build_mount(
            disk=persistent_disk.get('name'),
            path=os.path.join(providers_util.DATA_MOUNT_POINT,
                              persistent_disk_mount_param.docker_path),
            read_only=True)
        for persistent_disk, persistent_disk_mount_param in zip(
            persistent_disks, persistent_disk_mount_params)
    ]

    # The list of "actions" (1-based) will be:
    #   1- continuous copy of log files off to Cloud Storage
    #   2- prepare the shared mount point (write the user script)
    #   3- localize objects from Cloud Storage to block storage
    #   4- execute user command
    #   5- delocalize objects from block storage to Cloud Storage
    #   6- final copy of log files off to Cloud Storage
    #
    # If the user has requested an SSH server be started, it will be inserted
    # after logging is started, and all subsequent action numbers above will be
    # incremented by 1.
    # If the user has requested to mount one or more buckets, two actions per
    # bucket will be inserted after the prepare step, and all subsequent action
    # numbers will be incremented by the number of actions added.
    #
    # We need to track the action numbers specifically for the user action and
    # the final logging action.
    optional_actions = 0
    if job_resources.ssh:
      optional_actions += 1

    mount_actions = self._get_mount_actions(gcs_mounts, mnt_datadisk)
    optional_actions += len(mount_actions)

    user_action = 4 + optional_actions
    final_logging_action = 6 + optional_actions

    # Set up the commands and environment for the logging actions
    logging_cmd = _LOGGING_CMD.format(
        log_cp_fn=_GSUTIL_CP_FN,
        log_cp_cmd=_LOG_CP_CMD.format(
            user_action=user_action, logging_action='logging_action'))
    continuous_logging_cmd = _CONTINUOUS_LOGGING_CMD.format(
        log_msg_fn=_LOG_MSG_FN,
        log_cp_fn=_GSUTIL_CP_FN,
        log_cp_cmd=_LOG_CP_CMD.format(
            user_action=user_action,
            logging_action='continuous_logging_action'),
        final_logging_action=final_logging_action,
        log_interval=job_resources.log_interval or '60s')
    logging_env = self._get_logging_env(task_resources.logging_path.uri,
                                        user_project)

    # Set up command and environments for the prepare, localization, user,
    # and de-localization actions
    script_path = os.path.join(providers_util.SCRIPT_DIR, script.name)
    prepare_command = _PREPARE_CMD.format(
        log_msg_fn=_LOG_MSG_FN,
        mk_runtime_dirs=_MK_RUNTIME_DIRS_CMD,
        script_var=_SCRIPT_VARNAME,
        python_decode_script=_PYTHON_DECODE_SCRIPT,
        script_path=script_path,
        mk_io_dirs=_MK_IO_DIRS)

    prepare_env = self._get_prepare_env(script, task_view, inputs, outputs,
                                        mounts)
    localization_env = self._get_localization_env(inputs, user_project)
    user_environment = self._build_user_environment(envs, inputs, outputs,
                                                    mounts)
    delocalization_env = self._get_delocalization_env(outputs, user_project)

    # Build the list of actions
    actions = []
    actions.append(
        google_v2_pipelines.build_action(
            name='logging',
            flags='RUN_IN_BACKGROUND',
            image_uri=_CLOUD_SDK_IMAGE,
            environment=logging_env,
            entrypoint='/bin/bash',
            commands=['-c', continuous_logging_cmd]))

    if job_resources.ssh:
      actions.append(
          google_v2_pipelines.build_action(
              name='ssh',
              image_uri=_SSH_IMAGE,
              mounts=[mnt_datadisk],
              entrypoint='ssh-server',
              port_mappings={_DEFAULT_SSH_PORT: _DEFAULT_SSH_PORT},
              flags='RUN_IN_BACKGROUND'))

    actions.append(
        google_v2_pipelines.build_action(
            name='prepare',
            image_uri=_PYTHON_IMAGE,
            mounts=[mnt_datadisk],
            environment=prepare_env,
            entrypoint='/bin/bash',
            commands=['-c', prepare_command]),)

    actions.extend(mount_actions)

    actions.extend([
        google_v2_pipelines.build_action(
            name='localization',
            image_uri=_CLOUD_SDK_IMAGE,
            mounts=[mnt_datadisk],
            environment=localization_env,
            entrypoint='/bin/bash',
            commands=[
                '-c',
                _LOCALIZATION_CMD.format(
                    log_msg_fn=_LOG_MSG_FN,
                    recursive_cp_fn=_GSUTIL_RSYNC_FN,
                    cp_fn=_GSUTIL_CP_FN,
                    cp_loop=_LOCALIZATION_LOOP)
            ]),
        google_v2_pipelines.build_action(
            name='user-command',
            image_uri=job_resources.image,
            mounts=[mnt_datadisk] + persistent_disk_mounts,
            environment=user_environment,
            entrypoint='/usr/bin/env',
            commands=[
                'bash', '-c',
                _USER_CMD.format(
                    tmp_dir=providers_util.TMP_DIR,
                    working_dir=providers_util.WORKING_DIR,
                    user_script=script_path)
            ]),
        google_v2_pipelines.build_action(
            name='delocalization',
            image_uri=_CLOUD_SDK_IMAGE,
            mounts=[mnt_datadisk],
            environment=delocalization_env,
            entrypoint='/bin/bash',
            commands=[
                '-c',
                _LOCALIZATION_CMD.format(
                    log_msg_fn=_LOG_MSG_FN,
                    recursive_cp_fn=_GSUTIL_RSYNC_FN,
                    cp_fn=_GSUTIL_CP_FN,
                    cp_loop=_DELOCALIZATION_LOOP)
            ]),
        google_v2_pipelines.build_action(
            name='final_logging',
            flags='ALWAYS_RUN',
            image_uri=_CLOUD_SDK_IMAGE,
            environment=logging_env,
            entrypoint='/bin/bash',
            commands=['-c', logging_cmd]),
    ])

    assert len(actions) - 2 == user_action
    assert len(actions) == final_logging_action

    # Prepare the VM (resources) configuration
    disks = [
        google_v2_pipelines.build_disk(
            _DATA_DISK_NAME,
            job_resources.disk_size,
            source_image=None,
            disk_type=job_resources.disk_type or job_model.DEFAULT_DISK_TYPE)
    ]
    disks.extend(persistent_disks)
    network = google_v2_pipelines.build_network(
        job_resources.network, job_resources.subnetwork,
        job_resources.use_private_address)
    if job_resources.machine_type:
      machine_type = job_resources.machine_type
    elif job_resources.min_cores or job_resources.min_ram:
      machine_type = GoogleV2CustomMachine.build_machine_type(
          job_resources.min_cores, job_resources.min_ram)
    else:
      machine_type = job_model.DEFAULT_MACHINE_TYPE
    accelerators = None
    if job_resources.accelerator_type:
      accelerators = [
          google_v2_pipelines.build_accelerator(job_resources.accelerator_type,
                                                job_resources.accelerator_count)
      ]
    service_account = google_v2_pipelines.build_service_account(
        job_resources.service_account or 'default', scopes)

    resources = google_v2_pipelines.build_resources(
        self._project,
        job_resources.regions,
        google_base.get_zones(job_resources.zones),
        google_v2_pipelines.build_machine(
            network=network,
            machine_type=machine_type,
            preemptible=job_resources.preemptible,
            service_account=service_account,
            boot_disk_size_gb=job_resources.boot_disk_size,
            disks=disks,
            accelerators=accelerators,
            nvidia_driver_version=job_resources.nvidia_driver_version,
            labels=labels,
            cpu_platform=job_resources.cpu_platform),
    )

    # Build the pipeline request
    pipeline = google_v2_pipelines.build_pipeline(actions, resources, None,
                                                  job_resources.timeout)

    return {'pipeline': pipeline, 'labels': labels}