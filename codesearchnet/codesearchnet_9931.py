def configure_devel_job(
        config_url, rosdistro_name, source_build_name,
        repo_name, os_name, os_code_name, arch,
        pull_request=False,
        config=None, build_file=None,
        index=None, dist_file=None, dist_cache=None,
        jenkins=None, views=None,
        is_disabled=False,
        groovy_script=None,
        source_repository=None,
        build_targets=None,
        dry_run=False):
    """
    Configure a single Jenkins devel job.

    This includes the following steps:
    - clone the source repository to use
    - clone the ros_buildfarm repository
    - write the distribution repository keys into files
    - invoke the release/run_devel_job.py script
    """
    if config is None:
        config = get_config_index(config_url)
    if build_file is None:
        build_files = get_source_build_files(config, rosdistro_name)
        build_file = build_files[source_build_name]
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

    repo_names = dist_file.repositories.keys()

    if repo_name is not None:
        if repo_name not in repo_names:
            raise JobValidationError(
                "Invalid repository name '%s' " % repo_name +
                'choose one of the following: %s' %
                ', '.join(sorted(repo_names)))

        repo = dist_file.repositories[repo_name]
        if not repo.source_repository:
            raise JobValidationError(
                "Repository '%s' has no source section" % repo_name)
        if not repo.source_repository.version:
            raise JobValidationError(
                "Repository '%s' has no source version" % repo_name)
        source_repository = repo.source_repository

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

    if dist_cache is None and build_file.notify_maintainers:
        dist_cache = get_distribution_cache(index, rosdistro_name)
    if jenkins is None:
        from ros_buildfarm.jenkins import connect
        jenkins = connect(config.jenkins_url)
    if views is None:
        view_name = get_devel_view_name(
            rosdistro_name, source_build_name, pull_request=pull_request)
        configure_devel_view(jenkins, view_name, dry_run=dry_run)

    job_name = get_devel_job_name(
        rosdistro_name, source_build_name,
        repo_name, os_name, os_code_name, arch, pull_request)

    job_config = _get_devel_job_config(
        index, config, rosdistro_name, source_build_name,
        build_file, os_name, os_code_name, arch, source_repository,
        repo_name, pull_request, job_name, dist_cache=dist_cache,
        is_disabled=is_disabled)
    # jenkinsapi.jenkins.Jenkins evaluates to false if job count is zero
    if isinstance(jenkins, object) and jenkins is not False:
        from ros_buildfarm.jenkins import configure_job
        configure_job(jenkins, job_name, job_config, dry_run=dry_run)

    return job_name, job_config