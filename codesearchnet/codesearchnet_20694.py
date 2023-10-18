def get_all_files(folder):
    """
    Generator that loops through all absolute paths of the files within folder

    Parameters
    ----------
    folder: str
    Root folder start point for recursive search.

    Yields
    ------
    fpath: str
    Absolute path of one file in the folders
    """
    for path, dirlist, filelist in os.walk(folder):
        for fn in filelist:
            yield op.join(path, fn)