def configure_release_jobs(
        config_url, rosdistro_name, release_build_name, groovy_script=None,
        dry_run=False, whitelist_package_names=None):
    """
    Configure all Jenkins release jobs.

    L{configure_release_job} will be invoked for every released package and
    target which matches the build file criteria.

    Additionally a job to import Debian packages into the Debian repository is
    created.
    """
    config = get_config_index(config_url)
    build_files = get_release_build_files(config, rosdistro_name)
    build_file = build_files[release_build_name]

    index = get_index(config.rosdistro_index_url)

    # get targets
    platforms = []
    for os_name in build_file.targets.keys():
        for os_code_name in build_file.targets[os_name].keys():
            platforms.append((os_name, os_code_name))
    print('The build file contains the following targets:')
    for os_name, os_code_name in platforms:
        print('  - %s %s: %s' % (os_name, os_code_name, ', '.join(
            build_file.targets[os_name][os_code_name])))

    dist_file = get_distribution_file(index, rosdistro_name, build_file)
    if not dist_file:
        print('No distribution file matches the build file')
        return

    pkg_names = dist_file.release_packages.keys()
    filtered_pkg_names = build_file.filter_packages(pkg_names)
    explicitly_ignored_pkg_names = set(pkg_names) - set(filtered_pkg_names)
    if explicitly_ignored_pkg_names:
        print(('The following packages are being %s because of ' +
               'white-/blacklisting:') %
              ('ignored' if build_file.skip_ignored_packages else 'disabled'))
        for pkg_name in sorted(explicitly_ignored_pkg_names):
            print('  -', pkg_name)

    dist_cache = get_distribution_cache(index, rosdistro_name)

    if explicitly_ignored_pkg_names:
        # get direct dependencies from distro cache for each package
        direct_dependencies = {}
        for pkg_name in pkg_names:
            direct_dependencies[pkg_name] = _get_direct_dependencies(
                pkg_name, dist_cache, pkg_names) or set([])

        # find recursive downstream deps for all explicitly ignored packages
        ignored_pkg_names = set(explicitly_ignored_pkg_names)
        while True:
            implicitly_ignored_pkg_names = _get_downstream_package_names(
                ignored_pkg_names, direct_dependencies)
            if implicitly_ignored_pkg_names - ignored_pkg_names:
                ignored_pkg_names |= implicitly_ignored_pkg_names
                continue
            break
        implicitly_ignored_pkg_names = \
            ignored_pkg_names - explicitly_ignored_pkg_names

        if implicitly_ignored_pkg_names:
            print(('The following packages are being %s because their ' +
                   'dependencies are being ignored:') % ('ignored'
                  if build_file.skip_ignored_packages else 'disabled'))
            for pkg_name in sorted(implicitly_ignored_pkg_names):
                print('  -', pkg_name)
            filtered_pkg_names = \
                set(filtered_pkg_names) - implicitly_ignored_pkg_names

    # all further configuration will be handled by either the Jenkins API
    # or by a generated groovy script
    jenkins = False
    if groovy_script is None:
        from ros_buildfarm.jenkins import connect
        jenkins = connect(config.jenkins_url)

    all_view_configs = {}
    all_job_configs = OrderedDict()

    job_name, job_config = configure_import_package_job(
        config_url, rosdistro_name, release_build_name,
        config=config, build_file=build_file, jenkins=jenkins, dry_run=dry_run)
    if not jenkins:
        all_job_configs[job_name] = job_config

    job_name, job_config = configure_sync_packages_to_main_job(
        config_url, rosdistro_name, release_build_name,
        config=config, build_file=build_file, jenkins=jenkins, dry_run=dry_run)
    if not jenkins:
        all_job_configs[job_name] = job_config

    for os_name, os_code_name in platforms:
        for arch in sorted(build_file.targets[os_name][os_code_name]):
            job_name, job_config = configure_sync_packages_to_testing_job(
                config_url, rosdistro_name, release_build_name,
                os_code_name, arch,
                config=config, build_file=build_file, jenkins=jenkins,
                dry_run=dry_run)
            if not jenkins:
                all_job_configs[job_name] = job_config

    targets = []
    for os_name, os_code_name in platforms:
        targets.append((os_name, os_code_name, 'source'))
        for arch in build_file.targets[os_name][os_code_name]:
            targets.append((os_name, os_code_name, arch))
    views = configure_release_views(
        jenkins, rosdistro_name, release_build_name, targets,
        dry_run=dry_run)
    if not jenkins:
        all_view_configs.update(views)
    groovy_data = {
        'dry_run': dry_run,
        'expected_num_views': len(views),
    }

    # binary jobs must be generated in topological order
    from catkin_pkg.package import parse_package_string
    from ros_buildfarm.common import topological_order_packages
    pkgs = {}
    for pkg_name in pkg_names:
        if pkg_name not in dist_cache.release_package_xmls:
            print("Skipping package '%s': no released package.xml in cache" %
                  (pkg_name), file=sys.stderr)
            continue
        pkg_xml = dist_cache.release_package_xmls[pkg_name]
        pkg = parse_package_string(pkg_xml)
        pkgs[pkg_name] = pkg
    ordered_pkg_tuples = topological_order_packages(pkgs)

    other_build_files = [v for k, v in build_files.items() if k != release_build_name]

    all_source_job_names = []
    all_binary_job_names = []
    for pkg_name in [p.name for _, p in ordered_pkg_tuples]:
        if whitelist_package_names:
            if pkg_name not in whitelist_package_names:
                print("Skipping package '%s' not in the explicitly passed list" %
                      pkg_name, file=sys.stderr)
                continue

        pkg = dist_file.release_packages[pkg_name]
        repo_name = pkg.repository_name
        repo = dist_file.repositories[repo_name]
        is_disabled = pkg_name not in filtered_pkg_names
        if is_disabled and build_file.skip_ignored_packages:
            print("Skipping ignored package '%s' in repository '%s'" %
                  (pkg_name, repo_name), file=sys.stderr)
            continue
        if not repo.release_repository:
            print(("Skipping package '%s' in repository '%s': no release " +
                   "section") % (pkg_name, repo_name), file=sys.stderr)
            continue
        if not repo.release_repository.version:
            print(("Skipping package '%s' in repository '%s': no release " +
                   "version") % (pkg_name, repo_name), file=sys.stderr)
            continue

        for os_name, os_code_name in platforms:
            other_build_files_same_platform = []
            for other_build_file in other_build_files:
                if os_name not in other_build_file.targets:
                    continue
                if os_code_name not in other_build_file.targets[os_name]:
                    continue
                other_build_files_same_platform.append(other_build_file)

            try:
                source_job_names, binary_job_names, job_configs = \
                    configure_release_job(
                        config_url, rosdistro_name, release_build_name,
                        pkg_name, os_name, os_code_name,
                        config=config, build_file=build_file,
                        index=index, dist_file=dist_file,
                        dist_cache=dist_cache,
                        jenkins=jenkins, views=views,
                        generate_import_package_job=False,
                        generate_sync_packages_jobs=False,
                        is_disabled=is_disabled,
                        other_build_files_same_platform=other_build_files_same_platform,
                        groovy_script=groovy_script,
                        dry_run=dry_run)
                all_source_job_names += source_job_names
                all_binary_job_names += binary_job_names
                if groovy_script is not None:
                    print('Configuration for jobs: ' +
                          ', '.join(source_job_names + binary_job_names))
                    for source_job_name in source_job_names:
                        all_job_configs[source_job_name] = job_configs[source_job_name]
                    for binary_job_name in binary_job_names:
                        all_job_configs[binary_job_name] = job_configs[binary_job_name]
            except JobValidationError as e:
                print(e.message, file=sys.stderr)

    groovy_data['expected_num_jobs'] = len(all_job_configs)
    groovy_data['job_prefixes_and_names'] = {}

    # with an explicit list of packages we don't delete obsolete jobs
    if not whitelist_package_names:
        # delete obsolete binary jobs
        for os_name, os_code_name in platforms:
            for arch in build_file.targets[os_name][os_code_name]:
                binary_view = get_release_binary_view_name(
                    rosdistro_name, release_build_name,
                    os_name, os_code_name, arch)
                binary_job_prefix = '%s__' % binary_view

                excluded_job_names = set([
                    j for j in all_binary_job_names
                    if j.startswith(binary_job_prefix)])
                if groovy_script is None:
                    print("Removing obsolete binary jobs with prefix '%s'" %
                          binary_job_prefix)
                    from ros_buildfarm.jenkins import remove_jobs
                    remove_jobs(
                        jenkins, binary_job_prefix, excluded_job_names,
                        dry_run=dry_run)
                else:
                    binary_key = 'binary_%s_%s_%s' % \
                        (os_name, os_code_name, arch)
                    groovy_data['job_prefixes_and_names'][binary_key] = \
                        (binary_job_prefix, excluded_job_names)

        # delete obsolete source jobs
        # requires knowledge about all other release build files
        for os_name, os_code_name in platforms:
            other_source_job_names = []
            # get source job names for all other release build files
            for other_release_build_name in [
                    k for k in build_files.keys() if k != release_build_name]:
                other_build_file = build_files[other_release_build_name]
                other_dist_file = get_distribution_file(
                    index, rosdistro_name, other_build_file)
                if not other_dist_file:
                    continue

                if os_name not in other_build_file.targets or \
                        os_code_name not in other_build_file.targets[os_name]:
                    continue

                if other_build_file.skip_ignored_packages:
                    filtered_pkg_names = other_build_file.filter_packages(
                        pkg_names)
                else:
                    filtered_pkg_names = pkg_names
                for pkg_name in sorted(filtered_pkg_names):
                    pkg = other_dist_file.release_packages[pkg_name]
                    repo_name = pkg.repository_name
                    repo = other_dist_file.repositories[repo_name]
                    if not repo.release_repository:
                        continue
                    if not repo.release_repository.version:
                        continue

                    other_job_name = get_sourcedeb_job_name(
                        rosdistro_name, other_release_build_name,
                        pkg_name, os_name, os_code_name)
                    other_source_job_names.append(other_job_name)

            source_view_prefix = get_release_source_view_name(
                rosdistro_name, os_name, os_code_name)
            source_job_prefix = '%s__' % source_view_prefix
            excluded_job_names = set([
                j for j in (all_source_job_names + other_source_job_names)
                if j.startswith(source_job_prefix)])
            if groovy_script is None:
                print("Removing obsolete source jobs with prefix '%s'" %
                      source_job_prefix)
                from ros_buildfarm.jenkins import remove_jobs
                remove_jobs(
                    jenkins, source_job_prefix, excluded_job_names,
                    dry_run=dry_run)
            else:
                source_key = 'source_%s_%s' % (os_name, os_code_name)
                groovy_data['job_prefixes_and_names'][source_key] = (
                    source_job_prefix, excluded_job_names)

    if groovy_script is not None:
        print(
            "Writing groovy script '%s' to reconfigure %d views and %d jobs" %
            (groovy_script, len(all_view_configs), len(all_job_configs)))
        content = expand_template(
            'snippet/reconfigure_jobs.groovy.em', groovy_data)
        write_groovy_script_and_configs(
            groovy_script, content, all_job_configs,
            view_configs=all_view_configs)