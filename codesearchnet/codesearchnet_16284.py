def clean_path(a_path, force_os=None, force_start=None):
    """
    This function is used to normalize the path (of an output or
    dependency) and also provide the path in relative form. It is
    relative to the current working directory
    """
    if not force_start:
        force_start = os.curdir
    if force_os == "windows":
        import ntpath
        return ntpath.relpath(ntpath.normpath(a_path),
                             start=force_start)
    if force_os == "posix":
        import posixpath
        return posixpath.relpath(posixpath.normpath(a_path),
                                start=force_start)
    return os.path.relpath(os.path.normpath(a_path),
                          start=force_start)