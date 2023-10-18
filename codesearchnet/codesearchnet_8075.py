def norm_remote_path(path):
    """Normalize `path`.

    All remote paths are absolute.
    """
    path = os.path.normpath(path)
    if path.startswith(os.path.sep):
        return path[1:]
    else:
        return path