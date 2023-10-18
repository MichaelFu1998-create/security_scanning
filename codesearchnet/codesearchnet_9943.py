def configure_ci_jobs(
        config_url, rosdistro_name, ci_build_name,
        groovy_script=None, dry_run=False):
    """Configure all Jenkins CI jobs."""
    config = get_config_index(config_url)
    build_files = get_ci_build_files(config, rosdistro_name)
    build_file = build_files[ci_build_name]

    index = get_index(config.rosdistro_index_url)

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

    ci_view_name = get_ci_view_name(rosdistro_name)

    # all further configuration will be handled by either the Jenkins API
    # or by a generated groovy script
    from ros_buildfarm.jenkins import connect
    jenkins = connect(config.jenkins_url) if groovy_script is None else False

    view_configs = {}
    views = {
        ci_view_name: configure_ci_view(
            jenkins, ci_view_name, dry_run=dry_run)
    }
    if not jenkins:
        view_configs.update(views)
    groovy_data = {
        'dry_run': dry_run,
        'expected_num_views': len(view_configs),
    }

    ci_job_names = []
    job_configs = OrderedDict()

    is_disabled = False

    for os_name, os_code_name, arch in targets:
        try:
            job_name, job_config = configure_ci_job(
                config_url, rosdistro_name, ci_build_name,
                os_name, os_code_name, arch,
                config=config, build_file=build_file,
                index=index, dist_file=dist_file,
                jenkins=jenkins, views=views,
                is_disabled=is_disabled,
                groovy_script=groovy_script,
                dry_run=dry_run,
                trigger_timer=build_file.jenkins_job_schedule)
            ci_job_names.append(job_name)
            if groovy_script is not None:
                print("Configuration for job '%s'" % job_name)
                job_configs[job_name] = job_config
        except JobValidationError as e:
            print(e.message, file=sys.stderr)

    groovy_data['expected_num_jobs'] = len(job_configs)
    groovy_data['job_prefixes_and_names'] = {}

    if groovy_script is not None:
        print(
            "Writing groovy script '%s' to reconfigure %d jobs" %
            (groovy_script, len(job_configs)))
        content = expand_template(
            'snippet/reconfigure_jobs.groovy.em', groovy_data)
        write_groovy_script_and_configs(
            groovy_script, content, job_configs, view_configs)