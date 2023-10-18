def get_requirements(requirements_file):
    """
    Get the contents of a file listing the requirements
    """
    lines = open(requirements_file).readlines()
    dependencies = []
    dependency_links = []

    for line in lines:
        package = line.strip()
        if package.startswith('#'):
            # Skip pure comment lines
            continue

        if any(package.startswith(prefix) for prefix in VCS_PREFIXES):
            # VCS reference for dev purposes, expect a trailing comment
            # with the normal requirement
            package_link, __, package = package.rpartition('#')

            # Remove -e <version_control> string
            package_link = re.sub(r'(.*)(?P<dependency_link>https?.*$)', r'\g<dependency_link>', package_link)
            package = re.sub(r'(egg=)?(?P<package_name>.*)==.*$', r'\g<package_name>', package)
            package_version = re.sub(r'.*[^=]==', '', line.strip())

            if package:
                dependency_links.append(
                    '{package_link}#egg={package}-{package_version}'.format(
                        package_link=package_link,
                        package=package,
                        package_version=package_version,
                    )
                )
        else:
            # Ignore any trailing comment
            package, __, __ = package.partition('#')
            # Remove any whitespace and assume non-empty results are dependencies
            package = package.strip()

        if package:
            dependencies.append(package)
    return dependencies, dependency_links