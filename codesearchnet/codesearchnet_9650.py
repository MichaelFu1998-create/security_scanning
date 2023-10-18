def absolute_path(path=None, base_dir=None):
    """
    Return absolute path if path is local.

    Parameters:
    -----------
    path : path to file
    base_dir : base directory used for absolute path

    Returns:
    --------
    absolute path
    """
    if path_is_remote(path):
        return path
    else:
        if os.path.isabs(path):
            return path
        else:
            if base_dir is None or not os.path.isabs(base_dir):
                raise TypeError("base_dir must be an absolute path.")
            return os.path.abspath(os.path.join(base_dir, path))