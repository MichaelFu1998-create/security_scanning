def configure_release_job(
        config_url, rosdistro_name, release_build_name,
        pkg_name, os_name, os_code_name,
        config=None, build_file=None,
        index=None, dist_file=None, dist_cache=None,
        jenkins=None, views=None,
        generate_import_package_job=True,
        generate_sync_packages_jobs=True,
        is_disabled=False, other_build_files_same_platform=None,
        groovy_script=None,
        filter_arches=None,
        dry_run=False):
    """
    Configure a Jenkins release job.

    The following jobs are created for each package:
    - M source jobs, one for each OS node name
    - M * N binary jobs, one for each combination of OS code name and arch
    """
    if config is None:
        config = get_config_index(config_url)
    if build_file is None:
        build_files = get_release_build_files(config, rosdistro_name)
        build_file = build_files[release_build_name]

    if index is None:
        index = get_index(config.rosdistro_index_url)
    if dist_file is None:
        dist_file = get_distribution_file(index, rosdistro_name, build_file)
        if not dist_file:
            raise JobValidationError(
                'No distribution file matches the build file')

    pkg_names = dist_file.release_packages.keys()

    if pkg_name not in pkg_names:
        raise JobValidationError(
            "Invalid package name '%s' " % pkg_name +
            'choose one of the following: ' + ', '.join(sorted(pkg_names)))

    pkg = dist_file.release_packages[pkg_name]
    repo_name = pkg.repository_name
    repo = dist_file.repositories[repo_name]

    if not repo.release_repository:
        raise JobValidationError(
            "Repository '%s' has no release section" % repo_name)

    if not repo.release_repository.version:
        raise JobValidationError(
            "Repository '%s' has no release version" % repo_name)

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

    if dist_cache is None and \
            (build_file.notify_maintainers or
             build_file.abi_incompatibility_assumed):
        dist_cache = get_distribution_cache(index, rosdistro_name)
    if jenkins is None:
        from ros_buildfarm.jenkins import connect
        jenkins = connect(config.jenkins_url)
    if views is None:
        targets = []
        targets.append((os_name, os_code_name, 'source'))
        for arch in build_file.targets[os_name][os_code_name]:
            targets.append((os_name, os_code_name, arch))
        configure_release_views(
            jenkins, rosdistro_name, release_build_name, targets,
            dry_run=dry_run)

    if generate_import_package_job:
        configure_import_package_job(
            config_url, rosdistro_name, release_build_name,
            config=config, build_file=build_file, jenkins=jenkins,
            dry_run=dry_run)

    if generate_sync_packages_jobs:
        configure_sync_packages_to_main_job(
            config_url, rosdistro_name, release_build_name,
            config=config, build_file=build_file, jenkins=jenkins,
            dry_run=dry_run)
        for arch in build_file.targets[os_name][os_code_name]:
            configure_sync_packages_to_testing_job(
                config_url, rosdistro_name, release_build_name,
                os_code_name, arch,
                config=config, build_file=build_file, jenkins=jenkins,
                dry_run=dry_run)

    source_job_names = []
    binary_job_names = []
    job_configs = {}

    # sourcedeb job
    # since sourcedeb jobs are potentially being shared across multiple build
    # files the configuration has to take all of them into account in order to
    # generate a job which all build files agree on
    source_job_name = get_sourcedeb_job_name(
        rosdistro_name, release_build_name,
        pkg_name, os_name, os_code_name)

    # while the package is disabled in the current build file
    # it might be used by sibling build files
    is_source_disabled = is_disabled
    if is_source_disabled and other_build_files_same_platform:
        # check if sourcedeb job is used by any other build file with the same platform
        for other_build_file in other_build_files_same_platform:
            if other_build_file.filter_packages([pkg_name]):
                is_source_disabled = False
                break

    job_config = _get_sourcedeb_job_config(
        config_url, rosdistro_name, release_build_name,
        config, build_file, os_name, os_code_name,
        pkg_name, repo_name, repo.release_repository, dist_cache=dist_cache,
        is_disabled=is_source_disabled,
        other_build_files_same_platform=other_build_files_same_platform)
    # jenkinsapi.jenkins.Jenkins evaluates to false if job count is zero
    if isinstance(jenkins, object) and jenkins is not False:
        from ros_buildfarm.jenkins import configure_job
        configure_job(jenkins, source_job_name, job_config, dry_run=dry_run)
    source_job_names.append(source_job_name)
    job_configs[source_job_name] = job_config

    dependency_names = []
    if build_file.abi_incompatibility_assumed:
        dependency_names = _get_direct_dependencies(
            pkg_name, dist_cache, pkg_names)
        # if dependencies are not yet available in rosdistro cache
        # skip binary jobs
        if dependency_names is None:
            print(("Skipping binary jobs for package '%s' because it is not " +
                   "yet in the rosdistro cache") % pkg_name, file=sys.stderr)
            return source_job_names, binary_job_names, job_configs

    # binarydeb jobs
    for arch in build_file.targets[os_name][os_code_name]:
        if filter_arches and arch not in filter_arches:
            continue

        job_name = get_binarydeb_job_name(
            rosdistro_name, release_build_name,
            pkg_name, os_name, os_code_name, arch)

        upstream_job_names = [source_job_name] + [
            get_binarydeb_job_name(
                rosdistro_name, release_build_name,
                dependency_name, os_name, os_code_name, arch)
            for dependency_name in dependency_names]

        job_config = _get_binarydeb_job_config(
            config_url, rosdistro_name, release_build_name,
            config, build_file, os_name, os_code_name, arch,
            pkg_name, repo_name, repo.release_repository,
            dist_cache=dist_cache, upstream_job_names=upstream_job_names,
            is_disabled=is_disabled)
        # jenkinsapi.jenkins.Jenkins evaluates to false if job count is zero
        if isinstance(jenkins, object) and jenkins is not False:
            configure_job(jenkins, job_name, job_config, dry_run=dry_run)
        binary_job_names.append(job_name)
        job_configs[job_name] = job_config

    return source_job_names, binary_job_names, job_configs