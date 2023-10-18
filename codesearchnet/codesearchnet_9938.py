def get_version_status(
        package_descriptors, targets, repos_data,
        strip_version=False, strip_os_code_name=False):
    """
    For each package and target check if it is affected by a sync.

    This is the case when the package version in the testing repo is different
    from the version in the main repo.

    :return: a dict indexed by package names containing
      dicts indexed by targets containing
      a list of status strings (one for each repo)
    """
    status = {}
    for package_descriptor in package_descriptors.values():
        pkg_name = package_descriptor.pkg_name
        debian_pkg_name = package_descriptor.debian_pkg_name
        ref_version = package_descriptor.version
        if strip_version:
            ref_version = _strip_version_suffix(ref_version)

        status[pkg_name] = {}
        for target in targets:
            statuses = []
            for repo_data in repos_data:
                version = repo_data.get(target, {}).get(debian_pkg_name, None)
                if strip_version:
                    version = _strip_version_suffix(version)
                if strip_os_code_name:
                    version = _strip_os_code_name_suffix(
                        version, target.os_code_name)

                if ref_version:
                    if not version:
                        statuses.append('missing')
                    elif version.startswith(ref_version):  # including equal
                        statuses.append('equal')
                    else:
                        if _version_is_gt_other(version, ref_version):
                            statuses.append('higher')
                        else:
                            statuses.append('lower')
                else:
                    if not version:
                        statuses.append('ignore')
                    else:
                        statuses.append('obsolete')
            status[pkg_name][target] = statuses
    return status