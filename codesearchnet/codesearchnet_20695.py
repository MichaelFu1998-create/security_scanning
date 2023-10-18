def recursive_glob(base_directory, regex=''):
    """
    Uses glob to find all files or folders that match the regex
    starting from the base_directory.

    Parameters
    ----------
    base_directory: str

    regex: str

    Returns
    -------
    files: list

    """
    files = glob(op.join(base_directory, regex))
    for path, dirlist, filelist in os.walk(base_directory):
        for dir_name in dirlist:
            files.extend(glob(op.join(path, dir_name, regex)))

    return files