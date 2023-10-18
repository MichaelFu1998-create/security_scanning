def get_package_counts(package_descriptors, targets, repos_data):
    """
    Get the number of packages per target and repository.

    :return: a dict indexed by targets containing
      a list of integer values (one for each repo)
    """
    counts = {}
    for target in targets:
        counts[target] = [0] * len(repos_data)
    for package_descriptor in package_descriptors.values():
        debian_pkg_name = package_descriptor.debian_pkg_name

        for target in targets:
            for i, repo_data in enumerate(repos_data):
                version = repo_data.get(target, {}).get(debian_pkg_name, None)
                if version:
                    counts[target][i] += 1
    return counts