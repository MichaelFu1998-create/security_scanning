def get_folder_subpath(path, folder_depth):
    """
    Returns a folder path of path with depth given by folder_dept:

    Parameters
    ----------
    path: str

    folder_depth: int > 0

    Returns
    -------
    A folder path

    Example
    -------
    >>> get_folder_subpath('/home/user/mydoc/work/notes.txt', 3)
    >>> '/home/user/mydoc'
    """
    if path[0] == op.sep:
        folder_depth += 1

    return op.sep.join(path.split(op.sep)[0:folder_depth])