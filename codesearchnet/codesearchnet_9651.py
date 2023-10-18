def relative_path(path=None, base_dir=None):
    """
    Return relative path if path is local.

    Parameters:
    -----------
    path : path to file
    base_dir : directory where path sould be relative to

    Returns:
    --------
    relative path
    """
    if path_is_remote(path) or not os.path.isabs(path):
        return path
    else:
        return os.path.relpath(path, base_dir)