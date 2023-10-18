def get_version(filename, pattern):
    """Gets the current version from the specified file.

    This function assumes the file includes a string of the form::

        <pattern> = <version>

    """
    with open(filename) as f:
        match = re.search(r"^(\s*%s\s*=\s*')(.+?)(')(?sm)" % pattern, f.read())
    if match:
        before, version, after = match.groups()
        return version
    fail('Could not find {} in {}'.format(pattern, filename))