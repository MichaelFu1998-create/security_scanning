def get_sys_path(rcpath, app_name, section_name=None):
    """Return a folder path if it exists.

    First will check if it is an existing system path, if it is, will return it
    expanded and absoluted.

    If this fails will look for the rcpath variable in the app_name rcfiles or
    exclusively within the given section_name, if given.

    Parameters
    ----------
    rcpath: str
        Existing folder path or variable name in app_name rcfile with an
        existing one.

    section_name: str
        Name of a section in the app_name rcfile to look exclusively there for
        variable names.

    app_name: str
        Name of the application to look for rcfile configuration files.

    Returns
    -------
    sys_path: str
        A expanded absolute file or folder path if the path exists.

    Raises
    ------
    IOError if the proposed sys_path does not exist.
    """
    # first check if it is an existing path
    if op.exists(rcpath):
        return op.realpath(op.expanduser(rcpath))

    # look for the rcfile
    try:
        settings = rcfile(app_name, section_name)
    except:
        raise

    # look for the variable within the rcfile configutarions
    try:
        sys_path = op.expanduser(settings[rcpath])
    except KeyError:
        raise IOError('Could not find an existing variable with name {0} in'
                      ' section {1} of {2}rc config setup. Maybe it is a '
                      ' folder that could not be found.'.format(rcpath,
                                                                section_name,
                                                                app_name))
    # found the variable, now check if it is an existing path
    else:
        if not op.exists(sys_path):
            raise IOError('Could not find the path {3} indicated by the '
                          'variable {0} in section {1} of {2}rc config '
                          'setup.'.format(rcpath, section_name, app_name,
                                          sys_path))

        # expand the path and return
        return op.realpath(op.expanduser(sys_path))