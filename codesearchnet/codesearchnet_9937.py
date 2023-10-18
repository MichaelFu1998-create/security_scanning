def get_regressions(
        package_descriptors, targets,
        building_repo_data, testing_repo_data, main_repo_data):
    """
    For each package and target check if it is a regression.

    This is the case if the main repo contains a package version which is
    higher then in any of the other repos or if any of the other repos does not
    contain that package at all.

    :return: a dict indexed by package names containing
      dicts indexed by targets containing a boolean flag
    """
    regressions = {}
    for package_descriptor in package_descriptors.values():
        pkg_name = package_descriptor.pkg_name
        debian_pkg_name = package_descriptor.debian_pkg_name

        regressions[pkg_name] = {}
        for target in targets:
            regressions[pkg_name][target] = False
            main_version = \
                main_repo_data.get(target, {}).get(debian_pkg_name, None)
            if main_version is not None:
                main_ver_loose = LooseVersion(main_version)
                for repo_data in [building_repo_data, testing_repo_data]:
                    version = \
                        repo_data.get(target, {}).get(debian_pkg_name, None)
                    if not version or main_ver_loose > LooseVersion(version):
                        regressions[pkg_name][target] = True
    return regressions