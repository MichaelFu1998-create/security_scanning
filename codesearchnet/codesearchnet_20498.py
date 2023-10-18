def find_in_sections(var_name, app_name):
    """ Return the section and the value of the variable where the first
    var_name is found in the app_name rcfiles.

    Parameters
    ----------
    var_name: str
        Name of the variable to be searched for.

    app_name: str
        Name of the application to look for its rcfiles.

    Returns
    -------
    section_name: str
        Name of the section in the rcfiles where var_name was first found.

    var_value: str
        The value of the first variable with given var_name.
    """
    sections = get_sections(app_name)

    if not sections:
        raise ValueError('No sections found in {} rcfiles.'.format(app_name))

    for s in sections:
        try:
            var_value = get_rcfile_variable_value(var_name, section_name=s,
                                                  app_name=app_name)
        except:
            pass
        else:
            return s, var_value

    raise KeyError('No variable {} has been found in {} '
                   'rcfiles.'.format(var_name, app_name))