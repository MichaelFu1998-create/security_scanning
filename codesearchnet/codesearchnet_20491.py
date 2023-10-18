def get_temp_dir(prefix=None, basepath=None):
    """
    Uses tempfile to create a TemporaryDirectory using
    the default arguments.
    The folder is created using tempfile.mkdtemp() function.

    Parameters
    ----------
    prefix: str
    Name prefix for the temporary folder.

    basepath: str
    Directory where the new folder must be created.
    The default directory is chosen from a platform-dependent
    list, but the user of the application can control the
    directory location by setting the TMPDIR, TEMP or TMP
    environment variables.

    Returns
    -------
    folder object
    """
    if basepath is None:
        return tempfile.TemporaryDirectory(dir=basepath)
    else:
        return tempfile.TemporaryDirectory(prefix=prefix, dir=basepath)