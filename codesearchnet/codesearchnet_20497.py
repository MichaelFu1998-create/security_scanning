def get_rcfile_variable_value(var_name, app_name, section_name=None):
    """ Return the value of the variable in the section_name section of the
    app_name rc file.

    Parameters
    ----------
    var_name: str
        Name of the variable to be searched for.

    section_name: str
        Name of the section in the rcfiles.

    app_name: str
        Name of the application to look for its rcfiles.

    Returns
    -------
    var_value: str
        The value of the variable with given var_name.
    """
    cfg = get_rcfile_section(app_name, section_name)

    if var_name in cfg:
        raise KeyError('Option {} not found in {} '
                       'section.'.format(var_name, section_name))

    return cfg[var_name]