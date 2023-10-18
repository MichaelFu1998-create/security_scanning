def get_abspath(folderpath):
    """Returns the absolute path of folderpath.
    If the path does not exist, will raise IOError.
    """
    if not op.exists(folderpath):
        raise FolderNotFound(folderpath)

    return op.abspath(folderpath)