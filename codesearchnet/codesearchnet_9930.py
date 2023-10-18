def configure_devel_jobs(
        config_url, rosdistro_name, source_build_name, groovy_script=None,
        dry_run=False, whitelist_repository_names=None):
    """
    Configure all Jenkins devel jobs.

    L{configure_release_job} will be invoked for source repository and target
    which matches the build file criteria.
    """
    config = get_config_index(config_url)
    build_files = get_source_build_files(config, rosdistro_name)
    build_file = build_files[source_build_name]

    index = get_index(config.rosdistro_index_url)

    dist_cache = None
    if build_file.notify_maintainers:
        dist_cache = get_distribution_cache(index, rosdistro_name)

    # get targets
    targets = []
    for os_name in build_file.targets.keys():
        for os_code_name in build_file.targets[os_name].keys():
            for arch in build_file.targets[os_name][os_code_name]:
                targets.append((os_name, os_code_name, arch))
    print('The build file contains the following targets:')
    for os_name, os_code_name, arch in targets:
        print('  -', os_name, os_code_name, arch)

    dist_file = get_distribution_file(index, rosdistro_name, build_file)
    if not dist_file:
        print('No distribution file matches the build file')
        return

    devel_view_name = get_devel_view_name(
        rosdistro_name, source_build_name, pull_request=False)
    pull_request_view_name = get_devel_view_name(
        rosdistro_name, source_build_name, pull_request=True)

    # all further configuration will be handled by either the Jenkins API
    # or by a generated groovy script
    from ros_buildfarm.jenkins import connect
    jenkins = connect(config.jenkins_url) if groovy_script is None else False

    view_configs = {}
    views = {}
    if build_file.test_commits_force is not False:
        views[devel_view_name] = configure_devel_view(
            jenkins, devel_view_name, dry_run=dry_run)
    if build_file.test_pull_requests_force is not False:
        views[pull_request_view_name] = configure_devel_view(
            jenkins, pull_request_view_name, dry_run=dry_run)
    if not jenkins:
        view_configs.update(views)
    groovy_data = {
        'dry_run': dry_run,
        'expected_num_views': len(view_configs),
    }

    repo_names = dist_file.repositories.keys()
    filtered_repo_names = build_file.filter_repositories(repo_names)

    devel_job_names = []
    pull_request_job_names = []
    job_configs = OrderedDict()
    for repo_name in sorted(repo_names):
        if whitelist_repository_names:
            if repo_name not in whitelist_repository_names:
                print(
                    "Skipping repository '%s' not in explicitly passed list" %
                    repo_name, file=sys.stderr)
                continue

        is_disabled = repo_name not in filtered_repo_names
        if is_disabled and build_file.skip_ignored_repositories:
            print("Skipping ignored repository '%s'" % repo_name,
                  file=sys.stderr)
            continue

        repo = dist_file.repositories[repo_name]
        if not repo.source_repository:
            print("Skipping repository '%s': no source section" % repo_name)
            continue
        if not repo.source_repository.version:
            print("Skipping repository '%s': no source version" % repo_name)
            continue

        job_types = []
        # check for testing commits
        if build_file.test_commits_force is False:
            print(("Skipping repository '%s': 'test_commits' is forced to " +
                   "false in the build file") % repo_name)
        elif repo.source_repository.test_commits is False:
            print(("Skipping repository '%s': 'test_commits' of the " +
                   "repository set to false") % repo_name)
        elif repo.source_repository.test_commits is None and \
                not build_file.test_commits_default:
            print(("Skipping repository '%s': 'test_commits' defaults to " +
                   "false in the build file") % repo_name)
        else:
            job_types.append('commit')

        if not is_disabled:
            # check for testing pull requests
            if build_file.test_pull_requests_force is False:
                # print(("Skipping repository '%s': 'test_pull_requests' " +
                #        "is forced to false in the build file") % repo_name)
                pass
            elif repo.source_repository.test_pull_requests is False:
                # print(("Skipping repository '%s': 'test_pull_requests' of " +
                #        "the repository set to false") % repo_name)
                pass
            elif repo.source_repository.test_pull_requests is None and \
                    not build_file.test_pull_requests_default:
                # print(("Skipping repository '%s': 'test_pull_requests' " +
                #        "defaults to false in the build file") % repo_name)
                pass
            else:
                print("Pull request job for repository '%s'" % repo_name)
                job_types.append('pull_request')

        for job_type in job_types:
            pull_request = job_type == 'pull_request'
            for os_name, os_code_name, arch in targets:
                try:
                    job_name, job_config = configure_devel_job(
                        config_url, rosdistro_name, source_build_name,
                        repo_name, os_name, os_code_name, arch, pull_request,
                        config=config, build_file=build_file,
                        index=index, dist_file=dist_file,
                        dist_cache=dist_cache, jenkins=jenkins, views=views,
                        is_disabled=is_disabled,
                        groovy_script=groovy_script,
                        dry_run=dry_run)
                    if not pull_request:
                        devel_job_names.append(job_name)
                    else:
                        pull_request_job_names.append(job_name)
                    if groovy_script is not None:
                        print("Configuration for job '%s'" % job_name)
                        job_configs[job_name] = job_config
                except JobValidationError as e:
                    print(e.message, file=sys.stderr)

    groovy_data['expected_num_jobs'] = len(job_configs)
    groovy_data['job_prefixes_and_names'] = {}

    devel_job_prefix = '%s__' % devel_view_name
    pull_request_job_prefix = '%s__' % pull_request_view_name
    if not whitelist_repository_names:
        groovy_data['job_prefixes_and_names']['devel'] = \
            (devel_job_prefix, devel_job_names)
        groovy_data['job_prefixes_and_names']['pull_request'] = \
            (pull_request_job_prefix, pull_request_job_names)

        if groovy_script is None:
            # delete obsolete jobs in these views
            from ros_buildfarm.jenkins import remove_jobs
            print('Removing obsolete devel jobs')
            remove_jobs(
                jenkins, devel_job_prefix, devel_job_names, dry_run=dry_run)
            print('Removing obsolete pull request jobs')
            remove_jobs(
                jenkins, pull_request_job_prefix, pull_request_job_names,
                dry_run=dry_run)
    if groovy_script is not None:
        print(
            "Writing groovy script '%s' to reconfigure %d views and %d jobs" %
            (groovy_script, len(view_configs), len(job_configs)))
        content = expand_template(
            'snippet/reconfigure_jobs.groovy.em', groovy_data)
        write_groovy_script_and_configs(
            groovy_script, content, job_configs, view_configs=view_configs)