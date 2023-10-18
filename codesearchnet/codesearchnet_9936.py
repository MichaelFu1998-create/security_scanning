def get_affected_by_sync(
        package_descriptors, targets,
        testing_repo_data, main_repo_data):
    """
    For each package and target check if it is affected by a sync.

    This is the case when the package version in the testing repo is different
    from the version in the main repo.

    :return: a dict indexed by package names containing
      dicts indexed by targets containing a boolean flag
    """
    affected_by_sync = {}
    for package_descriptor in package_descriptors.values():
        pkg_name = package_descriptor.pkg_name
        debian_pkg_name = package_descriptor.debian_pkg_name

        affected_by_sync[pkg_name] = {}
        for target in targets:
            testing_version = _strip_version_suffix(
                testing_repo_data.get(target, {}).get(debian_pkg_name, None))
            main_version = _strip_version_suffix(
                main_repo_data.get(target, {}).get(debian_pkg_name, None))

            affected_by_sync[pkg_name][target] = \
                testing_version != main_version
    return affected_by_sync