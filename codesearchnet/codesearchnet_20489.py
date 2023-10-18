def remove_all(filelist, folder=''):
    """Deletes all files in filelist

    Parameters
    ----------
    filelist: list of str
        List of the file paths to be removed

    folder: str
        Path to be used as common directory for all file paths in filelist
    """
    if not folder:
        for f in filelist:
            os.remove(f)
    else:
        for f in filelist:
            os.remove(op.join(folder, f))