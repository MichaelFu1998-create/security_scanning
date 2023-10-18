def join_path_to_filelist(path, filelist):
    """Joins path to each line in filelist

    Parameters
    ----------
    path: str

    filelist: list of str

    Returns
    -------
    list of filepaths
    """
    return [op.join(path, str(item)) for item in filelist]