def sanitize_path(path):
    """Performs sanitation of the path after validating

    :param path: path to sanitize
    :return: path
    :raises:
        - InvalidPath if the path doesn't start with a slash
    """

    if path == '/':  # Nothing to do, just return
        return path

    if path[:1] != '/':
        raise InvalidPath('The path must start with a slash')

    # Deduplicate slashes in path
    path = re.sub(r'/+', '/', path)

    # Strip trailing slashes and return
    return path.rstrip('/')