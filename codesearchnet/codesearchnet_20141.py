def get_app_prefs(app=None):
    """Returns a dictionary with preferences for a certain app/module.

    :param str|unicode app:

    :rtype: dict

    """
    if app is None:

        with Frame(stepback=1) as frame:
            app = frame.f_globals['__name__'].split('.')[0]

    prefs = get_prefs()

    if app not in prefs:
        return {}

    return prefs[app]