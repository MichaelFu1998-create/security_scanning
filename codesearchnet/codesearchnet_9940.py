def get_homogeneous(package_descriptors, targets, repos_data):
    """
    For each package check if the version in one repo is equal for all targets.

    The version could be different in different repos though.

    :return: a dict indexed by package names containing a boolean flag
    """
    homogeneous = {}
    for package_descriptor in package_descriptors.values():
        pkg_name = package_descriptor.pkg_name
        debian_pkg_name = package_descriptor.debian_pkg_name

        versions = []
        for repo_data in repos_data:
            versions.append(set([]))
            for target in targets:
                version = _strip_version_suffix(
                    repo_data.get(target, {}).get(debian_pkg_name, None))
                versions[-1].add(version)
        homogeneous[pkg_name] = max([len(v) for v in versions]) == 1
    return homogeneous