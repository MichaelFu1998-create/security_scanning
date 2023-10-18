def listfilepath(p):
    """
    generator of list files in the path.
    filenames only
    """
    for entry in scandir.scandir(p):
        if entry.is_file():
            yield entry.path