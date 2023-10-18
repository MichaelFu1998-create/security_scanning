def expandvars_dict(settings):
    """Expands all environment variables in a settings dictionary."""
    return dict(
        (key, os.path.expandvars(value))
        for key, value in settings.iteritems()
    )