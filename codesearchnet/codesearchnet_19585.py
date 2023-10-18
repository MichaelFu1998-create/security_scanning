def listfile(p):
    """
    generator of list files in the path.
    filenames only
    """
    try:
        for entry in scandir.scandir(p):
            if entry.is_file():
                yield entry.name
    except OSError:
        return