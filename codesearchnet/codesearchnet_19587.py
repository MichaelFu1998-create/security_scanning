def listfolder(p):
    """
    generator of list folder in the path.
    folders only
    """
    for entry in scandir.scandir(p):
        if entry.is_dir():
            yield entry.name