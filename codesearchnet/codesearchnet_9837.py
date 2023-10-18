def get_lockdown_form(form_path):
    """Return a form class for a given string pointing to a lockdown form."""
    if not form_path:
        raise ImproperlyConfigured('No LOCKDOWN_FORM specified.')
    form_path_list = form_path.split(".")
    new_module = ".".join(form_path_list[:-1])
    attr = form_path_list[-1]
    try:
        mod = import_module(new_module)
    except (ImportError, ValueError):
        raise ImproperlyConfigured('Module configured in LOCKDOWN_FORM (%s) to'
                                   ' contain the form class couldn\'t be '
                                   'found.' % new_module)
    try:
        form = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('The module configured in LOCKDOWN_FORM '
                                   ' (%s) doesn\'t define a "%s" form.'
                                   % (new_module, attr))
    return form