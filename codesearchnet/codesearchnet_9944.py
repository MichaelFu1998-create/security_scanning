def configure_ci_job(
        config_url, rosdistro_name, ci_build_name,
        os_name, os_code_name, arch,
        config=None, build_file=None,
        index=None, dist_file=None,
        jenkins=None, views=None,
        is_disabled=False,
        groovy_script=None,
        build_targets=None,
        dry_run=False,
        underlay_source_paths=None,
        trigger_timer=None):
    """
    Configure a single Jenkins CI job.

    This includes the following steps:
    - clone the ros_buildfarm repository
    - write the distribution repository keys into files
    - invoke the ci/run_ci_job.py script
    """
    if config is None:
        config = get_config_index(config_url)
    if build_file is None:
        build_files = get_ci_build_files(config, rosdistro_name)
        build_file = build_files[ci_build_name]
    # Overwrite build_file.targets if build_targets is specified
    if build_targets is not None:
        build_file.targets = build_targets

    if index is None:
        index = get_index(config.rosdistro_index_url)
    if dist_file is None:
        dist_file = get_distribution_file(index, rosdistro_name, build_file)
        if not dist_file:
            raise JobValidationError(
                'No distribution file matches the build file')

    if os_name not in build_file.targets.keys():
        raise JobValidationError(
            "Invalid OS name '%s' " % os_name +
            'choose one of the following: ' +
            ', '.join(sorted(build_file.targets.keys())))
    if os_code_name not in build_file.targets[os_name].keys():
        raise JobValidationError(
            "Invalid OS code name '%s' " % os_code_name +
            'choose one of the following: ' +
            ', '.join(sorted(build_file.targets[os_name].keys())))
    if arch not in build_file.targets[os_name][os_code_name]:
        raise JobValidationError(
            "Invalid architecture '%s' " % arch +
            'choose one of the following: %s' % ', '.join(sorted(
                build_file.targets[os_name][os_code_name])))

    if len(build_file.underlay_from_ci_jobs) > 1:
        raise JobValidationError(
            'Only a single underlay job is currently supported, but the ' +
            'build file lists %d.' % len(build_file.underlay_from_ci_jobs))

    underlay_source_job = None
    if build_file.underlay_from_ci_jobs:
        underlay_source_job = get_ci_job_name(
            rosdistro_name, os_name, os_code_name, arch,
            build_file.underlay_from_ci_jobs[0])
        underlay_source_paths = (underlay_source_paths or []) + \
            ['$UNDERLAY_JOB_SPACE']

    if jenkins is None:
        from ros_buildfarm.jenkins import connect
        jenkins = connect(config.jenkins_url)
    if views is None:
        view_name = get_ci_view_name(rosdistro_name)
        configure_ci_view(jenkins, view_name, dry_run=dry_run)

    job_name = get_ci_job_name(
        rosdistro_name, os_name, os_code_name, arch, ci_build_name)

    job_config = _get_ci_job_config(
        index, rosdistro_name, build_file, os_name,
        os_code_name, arch,
        build_file.repos_files,
        underlay_source_job,
        underlay_source_paths,
        trigger_timer,
        is_disabled=is_disabled)
    # jenkinsapi.jenkins.Jenkins evaluates to false if job count is zero
    if isinstance(jenkins, object) and jenkins is not False:
        from ros_buildfarm.jenkins import configure_job
        configure_job(jenkins, job_name, job_config, dry_run=dry_run)

    return job_name, job_config