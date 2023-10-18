def get_last_file(input_dir, glob_pattern='*', key=op.getctime, reverse=True):
    """ Return the path to the latest file in `input_dir`.
     The `key` argument defines which information to use for sorting
     the list of files, could be:
        - creation date: os.path.getctime,
        - modification date: os.path.getmtime,
        etc.

    Parameters
    ----------
    input_dir: str
        Path to the folder where to perform the `glob`.

    glob_pattern: str
        `glob` Pattern to filter the files in `input_dir`.

    key: str
        Sorting key function

    reverse: bool
        Set to True if you want the sorting to be in decreasing order,
        False otherwise.

    Returns
    -------
    latest_filepath: str
        Path to the latest modified file in `input_dir`.
    """
    files = glob(op.join(input_dir, glob_pattern))
    files.sort(key=key, reverse=reverse)
    return files[0]