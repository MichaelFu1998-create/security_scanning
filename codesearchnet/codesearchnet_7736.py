def url_from_path(path):
    """Transform path to url, converting backslashes to slashes if needed."""

    if os.sep != '/':
        path = '/'.join(path.split(os.sep))
    return quote(path)