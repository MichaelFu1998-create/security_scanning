def configure_doc_job(
        config_url, rosdistro_name, doc_build_name,
        repo_name, os_name, os_code_name, arch,
        config=None, build_file=None,
        index=None, dist_file=None, dist_cache=None,
        jenkins=None, views=None,
        is_disabled=False,
        groovy_script=None,
        doc_repository=None,
        dry_run=False):
    """
    Configure a single Jenkins doc job.

    This includes the following steps:
    - clone the doc repository to use
    - clone the ros_buildfarm repository
    - write the distribution repository keys into files
    - invoke the run_doc_job.py script
    """
    if config is None:
        config = get_config_index(config_url)
    if build_file is None:
        build_files = get_doc_build_files(config, rosdistro_name)
        build_file = build_files[doc_build_name]

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
        if not repo.doc_repository:
            raise JobValidationError(
                "Repository '%s' has no doc section" % repo_name)
        if not repo.doc_repository.version:
            raise JobValidationError(
                "Repository '%s' has no doc version" % repo_name)
        doc_repository = repo.doc_repository

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
        view_name = get_doc_view_name(
            rosdistro_name, doc_build_name)
        configure_doc_view(jenkins, view_name, dry_run=dry_run)

    job_name = get_doc_job_name(
        rosdistro_name, doc_build_name,
        repo_name, os_name, os_code_name, arch)

    job_config = _get_doc_job_config(
        config, config_url, rosdistro_name, doc_build_name,
        build_file, os_name, os_code_name, arch, doc_repository,
        repo_name, dist_cache=dist_cache, is_disabled=is_disabled)
    # jenkinsapi.jenkins.Jenkins evaluates to false if job count is zero
    if isinstance(jenkins, object) and jenkins is not False:
        from ros_buildfarm.jenkins import configure_job
        configure_job(jenkins, job_name, job_config, dry_run=dry_run)

    return job_name, job_config