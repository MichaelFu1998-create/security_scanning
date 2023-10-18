def smkdirs(dpath, mode=0o777):
    """Safely make a full directory path if it doesn't exist.

    Parameters
    ----------
    dpath : str
        Path of directory/directories to create

    mode : int [default=0777]
        Permissions for the new directories

    See also
    --------
    os.makedirs
    """
    if not os.path.exists(dpath):
        os.makedirs(dpath, mode=mode)