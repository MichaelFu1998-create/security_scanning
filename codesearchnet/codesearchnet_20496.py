def get_rcfile_section(app_name, section_name):
    """ Return the dictionary containing the rcfile section configuration
    variables.

    Parameters
    ----------
    section_name: str
        Name of the section in the rcfiles.

    app_name: str
        Name of the application to look for its rcfiles.

    Returns
    -------
    settings: dict
        Dict with variable values
    """
    try:
        settings = rcfile(app_name, section_name)
    except IOError:
        raise
    except:
        raise KeyError('Error looking for section {} in {} '
                       ' rcfiles.'.format(section_name, app_name))
    else:
        return settings